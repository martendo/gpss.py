from datetime import datetime
from .parser import Parser
from .simulation import Simulation
from ._helpers import properties

parser = Parser()
simulation = Simulation()
warnings = properties["warnings"]
messages = properties["messages"]

def parse(*args, **kwargs):
	parser.parse(*args, **kwargs)

def run(*args, **kwargs):
	if len(args) + len(kwargs) > 0:
		parse(*args, **kwargs)
	simulation.run(parser)

def getReports():
	return simulation.reports

def createReport():
	s = "gpss.py Simulation Report"
	if parser.infile is not None:
		s += f" - {parser.infile}"
	s += "\nGenerated on "
	s += datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z").strip()
	s += "\n"
	s += "".join(getReports())
	return s
