def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        queues += f"""

  "{queue.name}":
    Maximum content: {queue.max_content}
    Average content: {(queue.utilization / simulation.time):.3f}
    Total entries: {queue.entries}
    Zero entries: {queue.zero_entries}
    Percent zeros: {(queue.zero_entries / queue.entries * 100):.2f}%
    Avg. time/Trans.: {(queue.utilization / queue.entries):.3f}
    Current content: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""

  "{facility.name}":
    Avg. utilization: {(facility.utilization / simulation.time * 100):.2f}%
    Entries: {facility.entries}
    Avg. time/Trans.: {(facility.utilization / facility.entries):.3f}
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
