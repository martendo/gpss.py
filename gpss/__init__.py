from datetime import datetime
from .parser import Parser
from .simulation import Simulation
from ._helpers import properties

parser = Parser()
simulation = Simulation()
warnings = properties["warnings"]

def parse(*args, **kwargs):
    parser.parse(*args, **kwargs)

def run(*args, **kwargs):
    if len(args) + len(kwargs) > 0:
        parse(*args, **kwargs)
    simulation.run(parser)

def getReports():
    return simulation.reports

def createReport():
    return f"""gpss.py Simulation Report - {parser.infile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")
    .strip()}
""" + "".join(getReports())
