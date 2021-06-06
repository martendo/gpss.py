from datetime import datetime

def createReport(simulation):
    queues = ""
    for name, queue in simulation.queues.items():
        queues += f"""  {name}
    MAXIMUM CONTENTS: {queue.max}
    CURRENT CONTENTS: {queue.contents}"""
    
    return f"""gpss.py Simulation Report - {simulation.parser.inputfile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")}

END TIME: {simulation.time}

FACILITIES: {len(simulation.facilities)}

QUEUES: {len(simulation.queues)}
{queues}"""
