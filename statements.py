from enum import Enum, auto

class Statements(Enum):
    SIMULATE = auto()
    START = auto()
    END = auto()
    GENERATE = auto()
    TERMINATE = auto()
    QUEUE = auto()
    DEPART = auto()
    SEIZE = auto()
    RELEASE = auto()
    ADVANCE = auto()
