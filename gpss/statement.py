from collections import namedtuple
from enum import Enum, auto

class Statement:
    def __init__(self, type_, name, operands, label, linenum, number):
        self.type = type_
        self.name = name,
        self.operands = operands
        self.label = label
        self.linenum = linenum
        self.number = number

class StatementType(Enum):
    # Commands
    END = auto()
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

COMMANDS = frozenset({
    StatementType.END,
    StatementType.SIMULATE,
    StatementType.START,
    StatementType.STORAGE,
})

BLOCKS = frozenset({
    StatementType.ADVANCE,
    StatementType.DEPART,
    StatementType.ENTER,
    StatementType.GENERATE,
    StatementType.LEAVE,
    StatementType.QUEUE,
    StatementType.RELEASE,
    StatementType.SEIZE,
    StatementType.TERMINATE,
    StatementType.TRANSFER,
})
