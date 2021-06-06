#!/usr/bin/env python3

import argparse
from debug import debugmsg, debugflag
from gpss_parser import Parser
from simulation import Simulation
from report import createReport
from error import ParserError, SimulationError

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file")
    argparser.add_argument("-o", "--output", help="print simulation report to output file")
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
        parser.parse(args.file)
    except ParserError as err:
        print(f"ERROR: Parser error:\n    {err}")
        return
    except FileNotFoundError as err:
        print(f"ERROR: File not found:\n    {err}")
        return
    
    # Run simulation
    simulation = Simulation()
    try:
        simulation.run(parser)
    except SimulationError as err:
        print(f"ERROR: Simulation error:\n    {err}")
        return
    
    if simulation.simulate:
        # Output report
        if args.output is not None:
            with open(args.output, "w") as file:
                file.write(createReport(simulation) + "\n")
        else:
            print("-" * 72)
            print(createReport(simulation))
            print("-" * 72)

if __name__ == "__main__":
    main()
