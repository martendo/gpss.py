from datetime import datetime

def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        queues += f"""
  {queue.name}
    MAXIMUM CONTENTS: {queue.max}
    CURRENT CONTENTS: {queue.contents}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""
  {facility.name}
    NUMBER ENTRIES: {facility.entries}
    AVAILBLE: {"no" if facility.is_in_use else "yes"}"""
    
    return f"""gpss.py Simulation Report - {simulation.parser.inputfile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")}

END TIME: {simulation.time}

FACILITIES: {len(simulation.facilities)}{facilities}

QUEUES: {len(simulation.queues)}{queues}"""
