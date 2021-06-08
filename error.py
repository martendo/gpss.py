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

def warn(filename, linenum, message):
    print(f"WARNING: {filename}({linenum}):\n    {message}")
