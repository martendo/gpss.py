from .error import ParserError, SimulationError, ExecutionWarning

properties = {
    "cli": False,
    "debug": False,
    "warnings": [],
}

# Print a message if using the CLI
def output(*args):
    if properties["cli"]:
        print(*args)

# Print a debug message if they are enabled
def debugmsg(*args):
    if properties["debug"]:
        output("DEBUG:", *args)

# Print a warning
def warn(filename, linenum, message):
    output(f"WARNING: {filename}({linenum}):\n    {message}")
    properties["warnings"].append(ExecutionWarning(
        filename,
        linenum,
        message,
    ))

# Print a parser error
def parser_error(parser, message):
    output(f"ERROR: Parser error: {parser.infile}({parser.linenum}):\n"
        f"    {message}")
    parser.errors.append(ParserError(
        parser.infile,
        parser.linenum,
        message,
    ))

# Print and raise a simulation error
def simulation_error(filename, linenum, message):
    output(f"ERROR: Simulation error: {filename}({linenum}):\n"
        f"    {message}")
    raise SimulationError(filename, linenum, message)
