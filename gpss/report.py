def createReport(simulation):
    queues = ""
    for queue in simulation.queues.values():
        queues += f"""

  "{queue.name}":
    Maximum content: {queue.max_content}
    Average content: {(queue.utilization / simulation.rel_time):.3f}
    Total entries: {queue.entries}
    Zero entries: {queue.zero_entries}
    Percent zeros: {(queue.zero_entries / queue.entries * 100):.2f}%
    Avg. time/Trans.: {(queue.utilization / queue.entries):.3f}
    Current content: {queue.content}"""
    
    facilities = ""
    for facility in simulation.facilities.values():
        facilities += f"""

  "{facility.name}":
    Avg. utilization: {(
        facility.utilization / simulation.rel_time * 100):.2f}%
    Entries: {facility.entries}
    Avg. time/Trans.: {(facility.utilization / facility.entries):.3f}
    Available: {"no" if facility.is_in_use else "yes"}"""
    
    storages = ""
    for storage in simulation.storages.values():
        storages += f"""

  "{storage.name}":
    Capacity: {storage.capacity}
    Average content: {(storage.utilization / simulation.rel_time):.3f}
    Avg. utilization: {(storage.utilization / (
        simulation.rel_time * storage.capacity) * 100):.2f}%
    Entries: {storage.entries}
    Avg. time/Trans.: {(storage.utilization / storage.entries):.3f}
    Maximum content: {storage.max_content}
    Current content: {storage.content}
    Remaining: {storage.available}
    Available: {"yes" if storage.available else "no"}"""
    
    return f"""
{f" SIMULATION {simulation.completed} ":=^72}

Relative Clock: {simulation.rel_time}
Absolute Clock: {simulation.time}

Facilities: {len(simulation.facilities)}{facilities}

Queues: {len(simulation.queues)}{queues}

Storages: {len(simulation.storages)}{storages}
"""
