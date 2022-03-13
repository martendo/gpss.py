from collections import deque, defaultdict
from random import Random
from .statement import Statement, StatementType, REDEFINABLE_STATEMENTS
from .transaction import Transaction, TransactionGenerator
from .queue import Queue
from .facility import Facility
from .storage import Storage
from .report import createReport
from ._helpers import debugmsg, simulation_error

# defaultdict that passes a Simulation instance and key to the default_factory
class entitydict(defaultdict):
	def __init__(self, simulation, *args, **kwargs):
		self.simulation = simulation
		super().__init__(*args, **kwargs)

	def __missing__(self, key):
		item = self[key] = self.default_factory(self.simulation, key)
		return item

class Simulation:
	RNG_SEED = 134630

	def __init__(self):
		self.running = False
		self.current_statement = None
		self.reports = []
		self.current_number = 0

	def __str__(self):
		s = "Simulation ("
		if not self.running:
			s += "not "
		s += "running)"
		return s

	def run(self, parser):
		self.parser = parser
		if len(self.parser.errors):
			# Couldn't parse the entire program successfully
			simulation_error(self.parser.infile, None, "Can't run a GPSS program with parser errors")

		self.program = self.parser.statements
		self.snamap = self.parser.snamap
		for entities in self.snamap.values():
			for entity in entities.values():
				entity.simulation = self
		self.labels = self.parser.labels

		self.initialize(first=True)

		# No START Command
		if self.current_statement is None:
			simulation_error(self.parser.infile, None, "Program contains no START Command")

		while self.current_statement < len(self.program):
			statement = self.program[self.current_statement]
			self.current_statement += 1

			# Start the simulation
			if statement.type is StatementType.START:
				# Set Termination Counter and Snap Interval Counter
				self.term_count = statement.operands[0]
				self.init_snap_count = statement.operands[2]
				self.snap_count = self.init_snap_count
				debugmsg("start:", self.term_count, self.snap_count)

				self.current_number += 1
				self.running = True
				while self.running:
					self.advance()

				if statement.operands[1] != "NP":
					self.reports.append(createReport(self))

			elif statement.type is StatementType.END:
				return True

			elif statement.type is StatementType.RESET:
				self.reset()
			elif statement.type is StatementType.CLEAR:
				self.initialize(first=False)

			# Replace an existing Block
			elif statement.type in REDEFINABLE_STATEMENTS:
				if statement.label is None:
					simulation_error(self.parser.infile, statement.linenum, "Replacement Block has no label")

				old_block = self.labels[statement.label]

				# GENERATE Blocks must be replaced with GENERATE Blocks
				if old_block.type is StatementType.GENERATE and statement.type is not StatementType.GENERATE:
					simulation_error(self.parser.infile, statement.linenum,
						"A GENERATE Block must be replaced with a GENERATE Block "
						f"(attempted replacement with {statement.type.name})")

				debugmsg("replace:", old_block.linenum, statement.linenum)

				# Take the old Block's place in the program
				self.program[old_block.number] = statement
				statement.linenum = old_block.linenum
				statement.number = old_block.number

		# Ran past end
		simulation_error(self.parser.infile, None, "Ran past the end of the program (missing END Command?)")

	def reset(self):
		# Reset only Relative Clock
		self.rel_time = 0
		# Clear entity statistics
		for queue in self.queues.values():
			queue.reset()
		for facility in self.facilities.values():
			facility.reset()
		for storage in self.storages.values():
			storage.reset()

	def initialize(self, first):
		# Clear leftover entities
		self.transactions = set()
		self.txn_generators = []
		self.queues = entitydict(self, Queue)
		self.facilities = entitydict(self, Facility)
		self.storages = {}
		self.events = []
		self.current_events = deque()
		if first:
			self.rngs = defaultdict(lambda: Random(self.RNG_SEED))
			self.current_statement = None

		# Reset Relative and Absolute Clocks
		self.rel_time = 0
		self.time = 0

		for statement in self.program:
			# Define a Transaction
			if statement.type is StatementType.GENERATE:
				debugmsg("transaction:", statement.operands)
				txn_generator = TransactionGenerator(self, statement.number, statement.operands)
				self.txn_generators.append(txn_generator)

			# Define a Storage's capacity
			elif statement.type is StatementType.STORAGE:
				self.storages[statement.label] = Storage(self, statement.label, statement.operands[0])
				debugmsg("storage:", statement.label, statement.operands[0])

			elif statement.type is StatementType.START:
				# First START Command, set as current statement
				if first and self.current_statement is None:
					self.current_statement = statement.number
				break

		# Prime Transaction generators
		for txn_generator in self.txn_generators:
			txn_generator.prime()

	def add_event(self, event):
		self.events.append(event)
		self.events.sort(key=lambda event: event.time, reverse=True)

	def advance(self):
		# Handle current events
		if len(self.current_events):
			current_events = self.current_events.copy()
			while len(current_events):
				current_events.popleft()()
			self.current_events = deque()

		# Handle next event
		try:
			event = self.events.pop()
		except IndexError:
			self.running = False
			return
		self.rel_time += event.time - self.time
		self.time = event.time
		event.func()

	def terminate(self, transaction, count):
		# Destroy the Transaction
		self.transactions.remove(transaction)

		# Update Termination Counter
		self.term_count -= count
		# Completed all Transactions, stop running
		if self.term_count < 1:
			self.running = False
			return

		# Update Snap Interval Counter
		if self.snap_count is not None:
			self.snap_count -= count
			if self.snap_count < 1:
				self.reports.append(createReport(self))
				self.snap_count = self.init_snap_count
