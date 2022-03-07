from ._helpers import simulation_error, warn

class Queue:
	def __init__(self, simulation, name):
		self.simulation = simulation
		self.name = name

		self.content = 0
		self.transactions = {}
		self.reset()

	def reset(self):
		self.entries = 0
		self.max_content = 0
		self.utilization = 0
		self.zero_entries = 0
		self.last_change = self.simulation.time

	@property
	def average_content(self):
		try:
			return self.utilization / self.simulation.rel_time
		except ZeroDivisionError:
			return 0

	@property
	def fraction_zeros(self):
		try:
			return self.zero_entries / self.entries
		except ZeroDivisionError:
			return -1

	@property
	def average_time(self):
		try:
			return self.utilization / self.entries
		except ZeroDivisionError:
			return -1

	@property
	def average_nz_time(self):
		try:
			return self.utilization / (self.entries - self.zero_entries)
		except ZeroDivisionError:
			return -1

	def __str__(self):
		return f"Queue \"{self.name}\": content {self.content}"

	def change(self):
		self.utilization += (self.simulation.time - self.last_change) * self.content
		self.last_change = self.simulation.time

	def join(self, transaction, content):
		self.change()
		self.content += content
		if self.content > self.max_content:
			self.max_content = self.content
		self.entries += content
		self.transactions[transaction] = self.simulation.time

	def depart(self, transaction, content):
		self.change()
		self.content -= content
		if self.content < 0:
			simulation_error(self.simulation.parser.infile, transaction.current_linenum,
				f"DEPART resulted in negative content in Queue \"{self.name}\" "
				f"({self.content + content} - {content} = {self.content})")
		try:
			if self.transactions[transaction] == self.simulation.time:
				self.zero_entries += content
		except KeyError:
			warn(self.simulation.parser.infile, transaction.current_linenum,
				f"Transaction DEPARTed Queue \"{self.name}\" without first joining it")
