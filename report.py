from datetime import datetime
from itertools import tee

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        # Calculate average content
        time_spanned = 0
        contentdur = 0
        for (content, time), (nextcontent, nexttime) in pairwise(queue.changes):
            duration = (nexttime or simulation.time) - time
            time_spanned += duration
            contentdur += content * duration
        average_content = contentdur / time_spanned
        
        queues += f"""

  "{queue.name}":
    Maximum content: {queue.max}
    Total entries: {queue.entries}
    Zero entries: {queue.zero_entries}
    Percent zeros: {(queue.zero_entries / queue.entries * 100):.2f}%
    Average content: {average_content:.2f}
    Current content: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""

  "{facility.name}":
    Entries: {facility.entries}
    Availble: {"no" if facility.is_in_use else "yes"}"""
    
    storages = ""
    for storage in simulation.storages.values():
        storages += f"""

  "{storage.name}":
    Capacity: {storage.capacity}
    Maximum usage: {storage.max}
    Entries: {storage.entries}
    Remaining: {storage.available}
    Available: {"yes" if storage.available else "no"}"""
    
    return f"""gpss.py Simulation Report - {simulation.parser.inputfile}
Generated on {datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S %Z")
    .strip()}

End time: {simulation.time}

Facilities: {len(simulation.facilities)}{facilities}

Queues: {len(simulation.queues)}{queues}

Storages: {len(simulation.storages)}{storages}"""
