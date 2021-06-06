import argparse
from debug import debugmsg, debugflag
from gpss_parser import Parser
from simulation import Simulation
from report import createReport
from error import SimulationError

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("inputfile")
    argparser.add_argument(
        "-d, --debug",
        action="store_true",
        dest="debug",
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
    parser.parse(args.inputfile)
    
    # Run simulation
    simulation = Simulation()
    try:
        simulation.run(parser)
    except SimulationError as err:
        print(f"ERROR: Simulation error:\n    {err}")
        return
    
    if simulation.simulate:
        # Output report
        print("-" * 72)
        print(createReport(simulation))
        print("-" * 72)

if __name__ == "__main__":
    main()
