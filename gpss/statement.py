from collections import namedtuple
from enum import Enum, auto

Statement = namedtuple("Statement",
    ["type", "name", "operands", "linenum", "number"])

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
