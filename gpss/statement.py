from collections import namedtuple
from enum import Enum, auto

class Statement:
	def __init__(self, type_, name, operands, label, linenum, number):
		self.type = type_
		self.name = name
		self.operands = operands
		self.label = label
		self.linenum = linenum
		self.number = number

	def __str__(self):
		return (f"Statement({self.type.name}, ({','.join(map(str, self.operands))}))")

	def refuse(self, simulation):
		if self.type is StatementType.SEIZE:
			# Refuse entry if Facility is currently in use
			return simulation.facilities[self.operands[0]].is_in_use
		elif self.type is StatementType.ENTER:
			# Refuse entry if Storage cannot satisfy demand
			return self.operands[1] > simulation.storages[self.operands[0]].available
		else:
			# Only ENTER and SEIZE Blocks can refuse entry
			return False

class StatementType(Enum):
	# Commands
	CLEAR = auto()
	END = auto()
	RESET = auto()
	SIMULATE = auto()
	START = auto()
	STORAGE = auto()

	# Blocks
	ADVANCE = auto()
	DEPART = auto()
	ENTER = auto()
	GENERATE = auto()
	LEAVE = auto()
	QUEUE = auto()
	RELEASE = auto()
	SEIZE = auto()
	TERMINATE = auto()
	TRANSFER = auto()

REDEFINABLE_STATEMENTS = frozenset({
	StatementType.ADVANCE,
	StatementType.DEPART,
	StatementType.ENTER,
	StatementType.GENERATE,
	StatementType.LEAVE,
	StatementType.QUEUE,
	StatementType.RELEASE,
	StatementType.SEIZE,
	StatementType.STORAGE,
	StatementType.TERMINATE,
	StatementType.TRANSFER,
})
