from datetime import datetime
from .parser import Parser
from .simulation import Simulation

# Errors that occur during simulation
class SimulationError(Exception):
    def __init__(self, filename, linenum, message):
        self.filename = filename
        self.linenum = linenum
        self.message = message

parser = Parser()
simulation = Simulation()

def parse(infile):
    parser.parse(infile)

def run(infile=None):
    if infile is not None:
        parse(infile)
    simulation.run(parser)

def getReports():
    return simulation.reports

def createReport():
    return f"""gpss.py Simulation Report - {parser.infile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")
    .strip()}
""" + "".join(getReports())
