from collections import defaultdict, deque
from ._helpers import debugmsg

class DelayChain:
	def __init__(self):
		self.content = defaultdict(deque)

	@property
	def line(self):
		return sorted(self.content.items(), reverse=True)

	def __str__(self):
		return f"DelayChain: content {len(self)} ({ {p: len(s) for p, s in self.line} })"

	def __len__(self):
		return sum(map(len, self.content.values()))

	def __iter__(self):
		for priority, section in self.line:
			for transaction in section:
				yield transaction

	def __delitem__(self, index):
		# Find priority section the Transaction is part of
		for priority, section in self.line:
			if index < len(section):
				break
			index -= len(section)
		else:
			# number is out of range of total length of Delay Chain
			raise IndexError("Transaction index out of range")

		del section[index]
		# If that section of the Delay Chain is now empty, remove it
		if not len(section):
			del self.content[priority]

	def append(self, transaction):
		# Add Transaction to its priority's section of the Delay Chain
		self.content[transaction.priority].append(transaction)

	def popleft(self):
		debugmsg("chain before:", self)

		# First-come, first-served, within priority class
		# Get highest priority in Delay Chain
		max_priority = max(self.content.keys())
		# Get the section of the Delay Chain of highest priority
		section = self.content[max_priority]
		# Remove the longest-waiting Transaction from the Delay Chain (first-come, first-served)
		transaction = section.popleft()

		# If that section of the Delay Chain is now empty, remove it
		if not len(section):
			del self.content[max_priority]

		debugmsg("chain after:", self)

		return transaction
