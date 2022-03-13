from sys import stderr
from .error import ParserError, SimulationError, ExecutionWarning

properties = {
	"cli": False,
	"debug": False,
	"warnings": [],
	"messages": [],
}

# Print out a formatted error message if using the CLI
def printerr(prefix, filename, linenum, message):
	if not properties["cli"]:
		return
	string = f"{prefix}: {filename}"
	if linenum is not None:
		string += f"({linenum})"
	string += f":\n    {message}"
	print(string, file=stderr)

# Print a debug message if they are enabled and using the CLI
def debugmsg(*args):
	if properties["debug"] and properties["cli"]:
		print("DEBUG:", *args)

# Print a warning
def warn(filename, linenum, message):
	printerr("WARNING", filename, linenum, message)
	warning = ExecutionWarning(filename, linenum, message)
	properties["warnings"].append(warning)
	properties["messages"].append(warning)

# Print a parser error
def parser_error(parser, message):
	printerr("ERROR: Parser error", parser.infile, parser.linenum, message)
	error = ParserError(parser.infile, parser.linenum, message)
	parser.errors.append(error)
	properties["messages"].append(error)

# Print and raise a simulation error
def simulation_error(filename, linenum, message):
	printerr("ERROR: Simulation error", filename, linenum, message)
	error = SimulationError(filename, linenum, message)
	properties["messages"].append(error)
	raise error
