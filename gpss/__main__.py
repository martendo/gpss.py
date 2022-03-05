import argparse
import gpss
from ._helpers import properties, debugmsg

def main():
	properties["cli"] = True

	argparser = argparse.ArgumentParser(prog="gpss.py",
		usage="python -m gpss [-S] [-d] [-o outfile] infile")
	argparser.add_argument("infile")
	argparser.add_argument("-o", "--output", metavar="outfile",
		help="print simulation report to output file instead of stdout")
	argparser.add_argument("-S", "--no-sim", dest="simulate", action="store_false",
		help="don't run the simulation but check for syntax errors")
	argparser.add_argument("-d", "--debug", action="store_true",
		help="print debug messages")
	argparser.add_argument("--version", action="version", version="v0.0.0")
	args = argparser.parse_args()
	debugmsg("args:", args)

	properties["debug"] = args.debug

	# Parse input file
	try:
		gpss.parse(args.infile)
	except FileNotFoundError as err:
		print(f"ERROR: File not found: {args.infile}:\n    {err.strerror}: {err.filename}")
		return
	if len(gpss.parser.errors):
		print(f"Parsing failed with {len(gpss.parser.errors)} error{'s' if len(gpss.parser.errors) != 1 else ''}")
		return

	if not args.simulate:
		return

	# Run simulation
	try:
		gpss.run()
	except gpss.error.SimulationError:
		return

	# Output report
	output = gpss.createReport()
	if args.debug:
		print("-" * 72)
	if args.output is not None:
		with open(args.output, "w") as file:
			file.write(output)
		print(f"Simulation report written to {args.output}")
	else:
		print(output, end="")

if __name__ == "__main__":
	main()
