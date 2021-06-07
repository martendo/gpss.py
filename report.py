from datetime import datetime

def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        queues += f"""
  {queue.name}
    MAXIMUM CONTENT: {queue.max}
    TOTAL ENTRIES: {queue.entries}
    CURRENT CONTENT: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""
  {facility.name}
    ENTRIES: {facility.entries}
    AVAILBLE: {"no" if facility.is_in_use else "yes"}"""
    
    storages = ""
    for storage in simulation.storages.values():
        storages += f"""
  {storage.name}
    CAPACITY: {storage.capacity}
    MAXIMUM USAGE: {storage.max}
    ENTRIES: {storage.entries}
    REMAINING: {storage.available}
    AVAILABLE: {"yes" if storage.available else "no"}"""
    
    return f"""gpss.py Simulation Report - {simulation.parser.inputfile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")}

END TIME: {simulation.time}

FACILITIES: {len(simulation.facilities)}{facilities}

QUEUES: {len(simulation.queues)}{queues}

STORAGES: {len(simulation.storages)}{storages}"""
