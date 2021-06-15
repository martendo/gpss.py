# Return formatted string if value is non-negative, otherwise return
# "N/A"
def na(value, fstring):
    if value >= 0:
        return fstring.format(value)
    else:
        return "N/A"

def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        queues += f"""

  "{queue.name}":
    Maximum content: {queue.max_content}
    Average content: {queue.average_content:.3f}
    Total entries: {queue.entries}
    Zero entries: {queue.zero_entries}
    Percent zeros: {na(queue.fraction_zeros * 100, "{:.2f}%")}
    Avg. time/Trans.: {na(queue.average_time, "{:.3f}")}
    Current content: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""

  "{facility.name}":
    Avg. utilization: {(facility.average_utilization * 100):.2f}%
    Entries: {facility.entries}
    Avg. time/Trans.: {na(facility.average_time, "{:.3f}")}
    Available: {"no" if facility.is_in_use else "yes"}"""
    
    storages = ""
    for storage in simulation.storages.values():
        storages += f"""

  "{storage.name}":
    Capacity: {storage.capacity}
    Average content: {storage.average_content:.3f}
    Avg. utilization: {(storage.average_utilization * 100):.2f}%
    Entries: {storage.entries}
    Avg. time/Trans.: {na(storage.average_time, "{:.3f}")}
    Maximum content: {storage.max_content}
    Current content: {storage.content}
    Remaining: {storage.available}
    Available: {"yes" if storage.available else "no"}"""
    
    return f"""
{f" SIMULATION {simulation.current_number} ":=^72}

Relative Clock: {simulation.rel_time}
Absolute Clock: {simulation.time}

Facilities: {len(simulation.facilities)}{facilities}

Queues: {len(simulation.queues)}{queues}

Storages: {len(simulation.storages)}{storages}
"""
