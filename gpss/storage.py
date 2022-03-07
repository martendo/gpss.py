from .delay_chain import DelayChain
from ._helpers import debugmsg, simulation_error

class Storage:
	def __init__(self, simulation, name, capacity):
		self.simulation = simulation
		self.name = name

		self.capacity = capacity
		self.available = self.capacity
		self.delaychain = DelayChain()
		self.demandmap = {}
		self.reset()

	def reset(self):
		self.entries = 0
		self.max_content = 0
		self.utilization = 0
		self.last_change = self.simulation.time

	@property
	def content(self):
		return self.capacity - self.available

	@property
	def average_content(self):
		try:
			return self.utilization / self.simulation.rel_time
		except ZeroDivisionError:
			return 0

	@property
	def average_utilization(self):
		try:
			return self.utilization / (self.simulation.rel_time * self.capacity)
		except ZeroDivisionError:
			return 0

	@property
	def average_time(self):
		try:
			return self.utilization / self.entries
		except ZeroDivisionError:
			return -1

	def __str__(self):
		return f"Storage \"{self.name}\": {self.content}/{self.capacity} used ({self.available} available)"

	def change(self):
		self.utilization += (self.simulation.time - self.last_change) * self.content
		self.last_change = self.simulation.time

	def enter(self, transaction, demand):
		if demand > self.capacity:
			simulation_error(self.simulation.parser.infile, transaction.current_linenum,
				f"Storage \"{self.name}\" does not have the capacity to satisfy the demand of {demand} "
				f"(capacity {self.capacity})")
		elif demand > self.available:
			# Storage cannot satisfy demand, add Transaction to delay chain
			self.delaychain.append(transaction)
			self.demandmap[transaction] = demand
			return False
		# Storage has sufficient availability
		self.engage(demand)
		return True

	def engage(self, demand):
		self.change()
		self.available -= demand
		if self.content > self.max_content:
			self.max_content = self.content
		self.entries += demand
		debugmsg("storage entered:", self.name, demand)

	def leave(self, transaction, units):
		self.change()
		self.available += units
		if self.available > self.capacity:
			simulation_error(self.simulation.parser.infile, transaction.current_linenum,
				f"LEAVE resulted in negative content in Storage \"{self.name}\" "
				f"({self.content + units} - {units} = {self.content})")
		debugmsg("storage left:", self.name, units)

		if not len(self.delaychain):
			# No Transactions in Delay Chain
			return
		# Allow first Transaction with demand that can be satisfied in Delay Chain to enter the Storage
		for i, transaction in enumerate(self.delaychain):
			demand = self.demandmap[transaction]
			if demand <= self.available:
				break
		else:
			# No Transaction's demand can be satisfied
			return
		del self.delaychain[i]
		del self.demandmap[transaction]
		self.engage(demand)
		transaction.update()
