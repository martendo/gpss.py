# Return formatted string if value is non-negative, otherwise return
# "N/A"
def na(value, fstring):
	if value >= 0:
		return fstring.format(value)
	else:
		return "N/A"

def createReport(simulation):
	queues = []
	for queue in simulation.queues.values():
		queues.append(
			"\n\n"
			f"  \"{queue.name}\":\n"
			f"    Maximum content: {queue.max_content}\n"
			f"    Average content: {queue.average_content:.3f}\n"
			f"    Total entries: {queue.entries}\n"
			f"    Zero entries: {queue.zero_entries}\n"
			f"    Percent zeros: {na(queue.fraction_zeros * 100, '{:.2f}%')}\n"
			f"    Avg. time/Trans.: {na(queue.average_time, '{:.3f}')}\n"
			f"    $ Avg. time/Trans.: {na(queue.average_nz_time, '{:.3f}')}\n"
			f"    Current content: {queue.content}"
		)

	facilities = []
	for facility in simulation.facilities.values():
		facilities.append(
			"\n\n"
			f"  \"{facility.name}\":\n"
			f"    Avg. utilization: {(facility.average_utilization * 100):.2f}%\n"
			f"    Entries: {facility.entries}\n"
			f"    Avg. time/Trans.: {na(facility.average_time, '{:.3f}')}\n"
			f"    Available: {'no' if facility.is_in_use else 'yes'}"
		)

	storages = []
	for storage in simulation.storages.values():
		storages.append(
			"\n\n"
			f"  \"{storage.name}\":\n"
			f"    Capacity: {storage.capacity}\n"
			f"    Average content: {storage.average_content:.3f}\n"
			f"    Avg. utilization: {(storage.average_utilization * 100):.2f}%\n"
			f"    Entries: {storage.entries}\n"
			f"    Avg. time/Trans.: {na(storage.average_time, '{:.3f}')}\n"
			f"    Maximum content: {storage.max_content}\n"
			f"    Current content: {storage.content}\n"
			f"    Remaining: {storage.available}\n"
			f"    Available: {'yes' if storage.available else 'no'}"
		)

	return (
		"\n"
		f"{f' SIMULATION {simulation.current_number} ':=^72}\n"
		"\n"
		f"Relative Clock: {simulation.rel_time}\n"
		f"Absolute Clock: {simulation.time}\n"
		"\n"
		f"Facilities: {len(simulation.facilities)}{''.join(facilities)}\n"
		"\n"
		f"Queues: {len(simulation.queues)}{''.join(queues)}\n"
		"\n"
		f"Storages: {len(simulation.storages)}{''.join(storages)}\n"
	)
