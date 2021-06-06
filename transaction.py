from random import randint
from debug import debugmsg
from error import SimulationError

class TransactionGenerator:
    def __init__(self, simulation, parameters, program):
        self.simulation = simulation
        self.program = program
        
        self.parameters = parameters
        self.interval, self.spread = self.parameters[0:2]
    
    def update_nexttime(self):
        # Set next generation time value
        if self.spread == 0:
            self.nexttime = self.simulation.time + self.interval
        else:
            self.nexttime = (self.simulation.time + self.interval
                + randint(-self.spread, +self.spread))
    
    def update(self):
        if self.simulation.time == self.nexttime:
            # Generate a new transaction
            debugmsg("generate:", self.simulation.time, self.parameters)
            transaction = Transaction(self.simulation, self.program)
            self.simulation.transactions.add(transaction)
            # Update next transaction generation time
            self.update_nexttime()

class Transaction:
    def __init__(self, simulation, program):
        self.program = program
        self.simulation = simulation
        self.currentcard = 0
        self.advancing = False
        self.delaying = False
    
    def update(self):
        if self.advancing:
            if self.simulation.time < self.advancetotime:
                return
            # Finished advancing, continue program
            self.advancing = False
        
        if self.delaying:
            # Waiting for a facility to become available
            return
        
        while True:
            # Execute next block
            block = self.program[self.currentcard]
            self.currentcard += 1
            
            if block.type == "TERMINATE":
                # Update transaction termination count
                try:
                    self.simulation.term_count -= block.parameters[0]
                except ValueError:
                    pass
                # Destroy this transaction
                self.simulation.transactions.remove(self)
                return
            
            elif block.type == "QUEUE":
                self.simulation.queues[block.parameters[0]].enter()
            
            elif block.type == "DEPART":
                self.simulation.queues[block.parameters[0]].leave()
            
            elif block.type == "ADVANCE":
                interval, spread = block.parameters[0:2]
                # Set time to advance to
                if spread == 0:
                    self.advancetotime = (self.simulation.time
                        + interval)
                else:
                    self.advancetotime = (self.simulation.time
                        + interval + randint(-spread, +spread))
                if self.advancetotime < self.simulation.time:
                    raise SimulationError(
                        "Cannot ADVANCE a negative amount of time "
                        f"({self.advancetotime - self.simulation.time})")
                elif self.advancetotime == self.simulation.time:
                    # ADVANCE 0 -> no-op
                    continue
                self.advancing = True
                return
            
            elif block.type == "SEIZE":
                # Use facility or enter delay chain if busy
                self.simulation.facilities[block.parameters[0]].seize(self)
            
            elif block.type == "RELEASE":
                self.simulation.facilities[block.parameters[0]].release()
