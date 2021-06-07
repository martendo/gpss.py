class Error(Exception):
    def __init__(self, linenum, message):
        self.linenum = linenum
        self.message = message

# Errors that occur in the parsing step
class ParserError(Error):
    pass

# Errors that occur during simulation
class SimulationError(Error):
    pass

# Errors that occur during simulation of an Entity, where the line
# number is unknown
class EntityError(SimulationError):
    def __init__(self, message):
        self.linenum = "unknown"
        self.message = message
