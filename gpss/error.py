class Error(Exception):
    def __init__(self, filename, linenum, message):
        self.filename = filename
        self.linenum = linenum
        self.message = message

# Errors that occur during simulation
class SimulationError(Error):
    pass

# Print a parser error
def parser_error(filename, linenum, message):
    print(f"ERROR: Parser error: {filename}({linenum}):\n"
        f"    {message}")

# Print and raise a simulation error
def simulation_error(filename, linenum, message):
    print(f"ERROR: Simulation error: {filename}({linenum}):\n"
        f"    {message}")
    raise SimulationError(filename, linenum, message)

# Print a warning
def warn(filename, linenum, message):
    print(f"WARNING: {filename}({linenum}):\n    {message}")
