import gpss

flags = {
    "debug": False,
}

# Print a debug message if they are enabled
def debugmsg(*args):
    if flags["debug"]:
        print("DEBUG:", *args)

# Print a warning
def warn(filename, linenum, message):
    print(f"WARNING: {filename}({linenum}):\n    {message}")

# Print a parser error
def parser_error(parser, message):
    print(f"ERROR: Parser error: {parser.infile}({parser.linenum}):\n"
        f"    {message}")
    parser.error_count += 1

# Print and raise a simulation error
def simulation_error(filename, linenum, message):
    print(f"ERROR: Simulation error: {filename}({linenum}):\n"
        f"    {message}")
    raise gpss.SimulationError(filename, linenum, message)
