from datetime import datetime

def createReport(simulation):
    return f"""gpss.py Simulation Report - {simulation.parser.inputfile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")}

END TIME: {simulation.time}

FACILITIES: {len(simulation.facilities)}

QUEUES: {len(simulation.queues)}"""
