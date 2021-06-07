from random import randint
from statements import Statements
from event import Event
from queue import Queue
from facility import Facility
from debug import debugmsg
from error import SimulationError, EntityError

class TransactionGenerator:
    def __init__(self, simulation, linenum, program, parameters):
        self.simulation = simulation
        self.linenum = linenum
        self.program = program
        
        self.parameters = parameters
        self.interval, self.spread = self.parameters[0:2]
    
    def add_next_event(self):
        # Add event to event list to generate next Transaction
        time = self.simulation.time + self.interval
        if self.spread != 0:
            time += randint(-self.spread, +self.spread)
        
        if time < self.simulation.time:
            raise SimulationError(self.linenum,
                "Cannot GENERATE a Transaction in a negative amount "
                f"of time ({time - self.simulation.time})")
        elif time == self.simulation.time:
            # Generate immediately, no need to add to event list
            self.generate()
        else:
            self.simulation.add_event(Event(time, self.generate))
    
    def generate(self):
        # Generate a new Transaction
        debugmsg("generate:", self.simulation.time, self.parameters)
        transaction = Transaction(self.simulation, self.program)
        self.simulation.transactions.add(transaction)
        # Add next Transaction generation event
        self.add_next_event()
        
        transaction.update()

class Transaction:
    def __init__(self, simulation, program):
        self.program = program
        self.simulation = simulation
        self.currentcard = 0
    
    def update(self):
        while True:
            # Execute next block
            block = self.program[self.currentcard]
            self.currentcard += 1
            
            if block.type == Statements.TERMINATE:
                # Update Transaction termination count
                self.simulation.term_count -= block.parameters[0]
                # Destroy this Transaction
                self.simulation.transactions.remove(self)
                return
            
            elif block.type in (Statements.QUEUE, Statements.DEPART):
                try:
                    queue = self.simulation.queues[block.parameters[0]]
                except KeyError:
                    # Queue doesn't exist yet -> create it
                    queue = Queue(block.parameters[0])
                    self.simulation.queues[queue.name] = queue
                
                if block.type == Statements.QUEUE:
                    queue.enter()
                else:
                    try:
                        queue.depart()
                    except EntityError as err:
                        raise SimulationError(block.linenum, err.message)
            
            elif block.type == Statements.ADVANCE:
                interval, spread = block.parameters[0:2]
                # Add event for end of delay
                time = self.simulation.time + interval
                if spread != 0:
                    time += randint(-spread, +spread)
                
                if time < self.simulation.time:
                    raise SimulationError(block.linenum,
                        "Cannot ADVANCE a negative amount of time "
                        f"({self.time - self.simulation.time})")
                elif time == self.simulation.time:
                    # ADVANCE 0 -> no-op
                    continue
                
                self.simulation.add_event(Event(time, self.update))
                return
            
            elif block.type in (Statements.SEIZE, Statements.RELEASE):
                try:
                    facility = self.simulation.facilities[block.parameters[0]]
                except KeyError:
                    # Facility doesn't exist yet -> create it
                    facility = Facility(block.parameters[0])
                    self.simulation.facilities[facility.name] = facility
                
                if block.type == Statements.SEIZE:
                    # Use Facility or enter Delay Chain if busy
                    if not facility.seize(self):
                        # Facility is busy -> wait
                        return
                else:
                    try:
                        facility.release(self)
                    except EntityError as err:
                        raise SimulationError(block.linenum, err.message)
            
            elif block.type == Statements.ENTER:
                # Enter Storage or enter Delay Chain if cannot satisfy
                # demand
                try:
                    entered = (self.simulation.storages[block.parameters[0]]
                        .enter(self, block.parameters[1]))
                except KeyError:
                    raise SimulationError(block.linenum, "No Storage "
                        f"named \"{block.parameters[0]}\"")
                except EntityError as err:
                    raise SimulationError(block.linenum, err.message)
                if not entered:
                    # Not enough Storage available
                    return
            
            elif block.type == Statements.LEAVE:
                try:
                    self.simulation.storages[block.parameters[0]].leave(
                        block.parameters[1])
                except KeyError:
                    raise SimulationError(block.linenum, "No Storage "
                        f"named \"{block.parameters[0]}\"")
                except EntityError as err:
                    raise SimulationError(block.linenum, err.message)
