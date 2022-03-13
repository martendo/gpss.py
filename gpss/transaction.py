from collections import namedtuple
from .statement import Statement, StatementType
from ._helpers import debugmsg, simulation_error

Event = namedtuple("Event", ["time", "func"])

class TransactionGenerator:
	def __init__(self, simulation, block_num, operands):
		self.simulation = simulation
		self.block = self.simulation.program[block_num]
		self.start_block = block_num + 1
		self.operands = operands
		self.generated = 0

	def __str__(self):
		return f"TransactionGenerator ({','.join(map(str, self.operands))})"

	def prime(self):
		# Add initial Transaction generation event using the Offset Interval
		self.add_next_event(self.operands[2])

	def add_next_event(self, time=None):
		# If reached generation Limit Count, stop
		if self.operands[3] is not None and self.generated >= self.operands[3]:
			return

		# Add event to event list to generate next Transaction
		if time is None:
			interval, spread = map(int, self.operands[0:2])
			time = self.simulation.time + interval
			if spread != 0:
				time += self.simulation.rngs[1].randint(-spread, spread)

		if time < self.simulation.time:
			simulation_error(self.simulation.parser.infile, self.block.linenum,
				f"Cannot GENERATE a Transaction in a negative amount of time ({time - self.simulation.time})")
		elif time == self.simulation.time and time is None:
			# Generate immediately, no need to add to event list
			self.generate()
		else:
			self.simulation.add_event(Event(time, self.generate))

	def generate(self):
		# Generate a new Transaction
		debugmsg("generate:", self.simulation.time, self.operands)
		transaction = Transaction(self.simulation, self.start_block, self.operands[4])
		self.simulation.transactions.add(transaction)
		self.generated += 1
		# Add next Transaction generation event
		self.add_next_event()

		transaction.update()

class Transaction:
	def __init__(self, simulation, start_block, priority):
		self.simulation = simulation
		self.current_block = start_block
		self.priority = priority

	def __str__(self):
		return f"Transaction: priority {self.priority}"

	def update(self):
		while True:
			# Execute next block
			block = self.simulation.program[self.current_block]
			self.current_block += 1

			self.current_linenum = block.linenum

			if block.type is StatementType.TERMINATE:
				self.simulation.terminate(self, block.operands[0])
				return

			elif block.type is StatementType.QUEUE:
				self.simulation.queues[block.operands[0]].join(self, block.operands[1])

			elif block.type is StatementType.DEPART:
				self.simulation.queues[block.operands[0]].depart(self, block.operands[1])

			elif block.type is StatementType.ADVANCE:
				interval, spread = map(int, block.operands[0:2])
				# Add event for end of delay
				time = self.simulation.time + interval
				if spread != 0:
					time += self.simulation.rngs[1].randint(-spread, spread)

				if time < self.simulation.time:
					simulation_error(self.simulation.parser.infile, block.linenum,
						f"Cannot ADVANCE a negative amount of time ({time - self.simulation.time})")
				elif time == self.simulation.time:
					# ADVANCE 0 -> no-op
					continue

				self.simulation.add_event(Event(time, self.update))
				return

			elif block.type is StatementType.SEIZE:
				# Use Facility or enter Delay Chain if busy
				if not self.simulation.facilities[block.operands[0]].seize(self):
					# Facility is busy -> wait
					return

			elif block.type is StatementType.RELEASE:
				self.simulation.facilities[block.operands[0]].release(self)

			elif block.type is StatementType.ENTER:
				# Enter Storage or enter Delay Chain if cannot satisfy demand
				try:
					if not (self.simulation.storages[block.operands[0]].enter(self, block.operands[1])):
						# Not enough Storage available
						return
				except KeyError:
					simulation_error(self.simulation.parser.infile, block.linenum,
						f"No Storage named \"{block.operands[0]}\"")

			elif block.type is StatementType.LEAVE:
				try:
					self.simulation.storages[block.operands[0]].leave(self, block.operands[1])
				except KeyError:
					simulation_error(self.simulation.parser.infile, block.linenum,
						f"No Storage named \"{block.operands[0]}\"")

			elif block.type is StatementType.TRANSFER:
				if block.operands[0] is None:
					# Unconditional transfer mode
					self.current_block = self.simulation.labels[block.operands[1]].number

				elif block.operands[0] == "BOTH":
					# BOTH mode
					if block.operands[1] != "":
						b_block = self.simulation.labels[block.operands[1]]
					else:
						# Use sequential Block
						b_block = self.simulation.program[self.current_block]
					c_block = self.simulation.labels[block.operands[2]]

					if not b_block.refuse(self.simulation):
						self.current_block = b_block.number
					elif not c_block.refuse(self.simulation):
						self.current_block = c_block.number
					else:
						# Refused entry to both Blocks, stay on this one
						self.current_block -= 1
						self.simulation.current_events.append(self.update)
						return

				else:
					# Statistical transfer mode
					if self.simulation.rngs[1].random() < block.operands[0]:
						new_block = block.operands[2]
					else:
						new_block = block.operands[1]
						if new_block == "":
							# Continue to sequential Block
							continue
					self.current_block = self.simulation.labels[new_block].number
