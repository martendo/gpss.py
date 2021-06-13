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
        time_spanned = simulation.time - queue.changes[0][1]
        contentdur = 0
        for (content, time), (nextcontent, nexttime) in pairwise(queue.changes):
            if nexttime is None:
                nexttime = simulation.time
            contentdur += content * (nexttime - time)
        average_content = contentdur / time_spanned
        
        queues += f"""

  "{queue.name}":
    Maximum content: {queue.max_content}
    Average content: {average_content:.3f}
    Total entries: {queue.entries}
    Zero entries: {queue.zero_entries}
    Percent zeros: {(queue.zero_entries / queue.entries * 100):.2f}%
    Current content: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""

  "{facility.name}":
    Entries: {facility.entries}
    Available: {"no" if facility.is_in_use else "yes"}"""
    
    storages = ""
    for storage in simulation.storages.values():
        storages += f"""

  "{storage.name}":
    Capacity: {storage.capacity}
    Entries: {storage.entries}
    Maximum content: {storage.max_content}
    Current content: {storage.content}
    Remaining: {storage.available}
    Available: {"yes" if storage.available else "no"}"""
    
    return f"""
{f" SIMULATION {simulation.completed} ":=^72}

End time: {simulation.time}

Facilities: {len(simulation.facilities)}{facilities}

Queues: {len(simulation.queues)}{queues}

Storages: {len(simulation.storages)}{storages}
"""
