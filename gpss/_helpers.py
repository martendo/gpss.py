import gpss

flags = {
    "cli": False,
    "debug": False,
}

# Print a message if using the CLI
def output(*args):
    if flags["cli"]:
        print(*args)

# Print a debug message if they are enabled
def debugmsg(*args):
    if flags["debug"]:
        output("DEBUG:", *args)

# Print a warning
def warn(filename, linenum, message):
    output(f"WARNING: {filename}({linenum}):\n    {message}")

# Print a parser error
def parser_error(parser, message):
    output(f"ERROR: Parser error: {parser.infile}({parser.linenum}):\n"
        f"    {message}")
    parser.error_count += 1

# Print and raise a simulation error
def simulation_error(filename, linenum, message):
    output(f"ERROR: Simulation error: {filename}({linenum}):\n"
        f"    {message}")
    raise gpss.SimulationError(filename, linenum, message)
