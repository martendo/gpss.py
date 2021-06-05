import argparse
from debug import debugmsg, debugflag

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

if __name__ == "__main__":
    main()
