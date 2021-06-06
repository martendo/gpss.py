from random import randint
from statements import Statements
from event import Event
from debug import debugmsg
from error import SimulationError

class TransactionGenerator:
    def __init__(self, simulation, parameters, program):
        self.simulation = simulation
        self.program = program
        
        self.parameters = parameters
        self.interval, self.spread = self.parameters[0:2]
    
    def add_next_event(self):
        # Add event to event list to generate next transaction
        time = self.simulation.time + self.interval
        if self.spread != 0:
            time += randint(-self.spread, +self.spread)
        self.simulation.add_event(Event(time, self.generate))
    
    def generate(self):
        # Generate a new transaction
        debugmsg("generate:", self.simulation.time, self.parameters)
        transaction = Transaction(self.simulation, self.program)
        self.simulation.transactions.add(transaction)
        # Add next transaction generation event
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
                # Update transaction termination count
                self.simulation.term_count -= block.parameters[0]
                # Destroy this transaction
                self.simulation.transactions.remove(self)
                return
            
            elif block.type == Statements.QUEUE:
                self.simulation.queues[block.parameters[0]].enter()
            
            elif block.type == Statements.DEPART:
                self.simulation.queues[block.parameters[0]].leave()
            
            elif block.type == Statements.ADVANCE:
                interval, spread = block.parameters[0:2]
                # Add event for end of delay
                time = self.simulation.time + interval
                if spread != 0:
                    time += randint(-spread, +spread)
                
                if time < self.simulation.time:
                    raise SimulationError(
                        "Cannot ADVANCE a negative amount of time "
                        f"({self.time - self.simulation.time})")
                elif time == self.simulation.time:
                    # ADVANCE 0 -> no-op
                    continue
                
                self.simulation.add_event(Event(time, self.update))
                return
            
            elif block.type == Statements.SEIZE:
                # Use facility or enter delay chain if busy
                if not self.simulation.facilities[block.parameters[0]].seize(self):
                    # Facility is busy -> wait
                    return
            
            elif block.type == Statements.RELEASE:
                self.simulation.facilities[block.parameters[0]].release()
            
            elif block.type == Statements.ENTER:
                # Enter storage or enter delay chain if cannot satisfy
                # demand
                try:
                    entered = (self.simulation.storages[block.parameters[0]]
                        .enter(self, block.parameters[1]))
                except KeyError:
                    raise SimulationError("No Storage named "
                        f"\"{block.parameters[0]}\"")
                if not entered:
                    # Not enough storage available
                    return
            
            elif block.type == Statements.LEAVE:
                try:
                    self.simulation.storages[block.parameters[0]].leave(
                        block.parameters[1])
                except KeyError:
                    raise SimulationError("No Storage named "
                        f"\"{block.parameters[0]}\"")
