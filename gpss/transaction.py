from random import randint
from .statement import Statement, StatementType
from .event import Event
from .queue import Queue
from .facility import Facility
from .debug import debugmsg
from .error import simulation_error

class TransactionGenerator:
    def __init__(self, simulation, block_num, operands):
        self.simulation = simulation
        self.block = self.simulation.program[block_num]
        self.start_block = block_num + 1
        self.operands = operands
        self.generated = 0
    
    def __repr__(self):
        return f"TransactionGenerator({','.join(map(str, self.operands))})"
    
    def prime(self):
        # Add initial Transaction generation event using the Offset
        # Interval
        self.add_next_event(self.operands[2])
    
    def add_next_event(self, time=None):
        # If reached generation Limit Count, stop
        if (self.operands[3] is not None
                and self.generated >= self.operands[3]):
            return
        
        # Add event to event list to generate next Transaction
        if time is None:
            time = self.simulation.time + self.operands[0]
            if self.operands[1] != 0:
                time += randint(-self.operands[1], +self.operands[1])
        
        if time < self.simulation.time:
            simulation_error(self.simulation.parser.infile,
                self.block.linenum,
                "Cannot GENERATE a Transaction in a negative amount "
                f"of time ({time - self.simulation.time})")
        elif time == self.simulation.time:
            # Generate immediately, no need to add to event list
            self.generate()
        else:
            self.simulation.add_event(Event(time, self.generate))
    
    def generate(self):
        # Generate a new Transaction
        debugmsg("generate:", self.simulation.time, self.operands)
        transaction = Transaction(self.simulation, self.start_block,
            self.operands[4])
        self.simulation.transactions.add(transaction)
        self.generated += 1
        # Add next Transaction generation event
        self.add_next_event()
        
        transaction.update()

class Transaction:
    def __init__(self, simulation, start_block, priority):
        self.simulation = simulation
        self.current_block = start_block
        self.priority = priority
    
    def __repr__(self):
        return f"Transaction({self.priority})"
    
    def update(self):
        while True:
            # Execute next block
            block = self.simulation.program[self.current_block]
            self.current_block += 1
            
            self.current_linenum = block.linenum
            
            if block.type is StatementType.TERMINATE:
                self.simulation.terminate(self, block.operands[0])
                return
            
            elif block.type in (StatementType.QUEUE, StatementType.DEPART):
                try:
                    queue = self.simulation.queues[block.operands[0]]
                except KeyError:
                    # Queue doesn't exist yet -> create it
                    queue = Queue(self.simulation, block.operands[0])
                    self.simulation.queues[queue.name] = queue
                
                if block.type is StatementType.QUEUE:
                    queue.join(self, block.operands[1])
                else:
                    queue.depart(self, block.operands[1])
            
            elif block.type is StatementType.ADVANCE:
                interval, spread = block.operands[0:2]
                # Add event for end of delay
                time = self.simulation.time + interval
                if spread != 0:
                    time += randint(-spread, +spread)
                
                if time < self.simulation.time:
                    simulation_error(self.simulation.parser.infile,
                        block.linenum,
                        "Cannot ADVANCE a negative amount of time "
                        f"({self.time - self.simulation.time})")
                elif time == self.simulation.time:
                    # ADVANCE 0 -> no-op
                    continue
                
                self.simulation.add_event(Event(time, self.update))
                return
            
            elif block.type in (StatementType.SEIZE, StatementType.RELEASE):
                try:
                    facility = self.simulation.facilities[block.operands[0]]
                except KeyError:
                    # Facility doesn't exist yet -> create it
                    facility = Facility(self.simulation, block.operands[0])
                    self.simulation.facilities[facility.name] = facility
                
                if block.type is StatementType.SEIZE:
                    # Use Facility or enter Delay Chain if busy
                    if not facility.seize(self):
                        # Facility is busy -> wait
                        return
                else:
                    facility.release(self)
            
            elif block.type is StatementType.ENTER:
                # Enter Storage or enter Delay Chain if cannot satisfy
                # demand
                try:
                    entered = (self.simulation.storages[block.operands[0]]
                        .enter(self, block.operands[1]))
                except KeyError:
                    simulation_error(self.simulation.parser.infile,
                        block.linenum,
                        f"No Storage named \"{block.operands[0]}\"")
                if not entered:
                    # Not enough Storage available
                    return
            
            elif block.type is StatementType.LEAVE:
                try:
                    self.simulation.storages[block.operands[0]].leave(
                        self, block.operands[1])
                except KeyError:
                    simulation_error(self.simulation.parser.infile,
                        block.linenum,
                        f"No Storage named \"{block.operands[0]}\"")
            
            elif block.type is StatementType.TRANSFER:
                self.current_block = self.simulation.labels[block.operands[1]].number
