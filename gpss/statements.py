from enum import Enum, auto

class Statements(Enum):
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
