import argparse
from .debug import debugmsg, debugflag
from .parser import Parser
from .simulation import Simulation
from .report import createReport
from .error import SimulationError

def main():
    argparser = argparse.ArgumentParser(
        prog="gpss.py",
        usage="python -m gpss [-S] [-d] [-o outfile] infile",
    )
    argparser.add_argument("infile")
    argparser.add_argument(
        "-o", "--output",
        metavar="outfile",
        help="print simulation report to output file"
    )
    argparser.add_argument(
        "-S", "--no-sim",
        dest="simulate",
        action="store_false",
        help="don't run the simulation but check for syntax errors",
    )
    argparser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="print debug messages",
    )
    argparser.add_argument(
        "--version",
        action="version",
        version="v0.0.0",
    )
    args = argparser.parse_args()
    debugflag["debug"] = args.debug
    debugmsg("args:", args)
    
    # Parse input file
    parser = Parser()
    try:
        parser.parse(args.infile)
    except FileNotFoundError as err:
        print(f"ERROR: File not found: {args.infile}:\n"
            f"    {err.strerror}: {err.filename}")
        return
    if parser.error_count > 0:
        print(f"Parsing failed with {parser.error_count} "
            f"error{'s' if parser.error_count != 1 else ''}")
        return
    
    if not args.simulate:
        return
    
    # Run simulation
    simulation = Simulation()
    try:
        simulation.run(parser)
    except SimulationError:
        return
    
    # Output report
    if args.output is not None:
        with open(args.output, "w") as file:
            file.write(createReport(simulation) + "\n")
        print("Simulation completed and report written to "
            + args.output)
    else:
        print("-" * 72)
        print(createReport(simulation))
        print("-" * 72)

if __name__ == "__main__":
    main()
