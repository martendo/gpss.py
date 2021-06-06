from random import randint
from debug import debugmsg
from error import SimulationError

class TransactionGenerator:
    def __init__(self, simulation, parameters, program):
        self.simulation = simulation
        self.program = program
        
        self.parameters = parameters
        self.interval = int(self.parameters[0])
        # Default spread modifier to 0
        try:
            self.spread = int(self.parameters[1])
        except IndexError:
            self.spread = 0
    
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
            
            if block[0] == "TERMINATE":
                # Update transaction termination count
                try:
                    self.simulation.term_count -= int(block[1][0])
                except ValueError:
                    pass
                # Destroy this transaction
                self.simulation.transactions.remove(self)
                return
            
            elif block[0] == "QUEUE":
                self.simulation.queues[block[1][0]].enter()
            
            elif block[0] == "DEPART":
                self.simulation.queues[block[1][0]].leave()
            
            elif block[0] == "ADVANCE":
                try:
                    spread = int(block[1][1])
                except IndexError:
                    spread = 0
                
                # Set time to advance to
                if spread == 0:
                    self.advancetotime = (self.simulation.time
                        + int(block[1][0]))
                else:
                    self.advancetotime = (self.simulation.time
                        + int(block[1][0]) + randint(-spread, +spread))
                if self.advancetotime < self.simulation.time:
                    raise SimulationError(
                        "Cannot ADVANCE a negative amount of time "
                        f"({self.advancetotime - self.simulation.time})")
                elif self.advancetotime == self.simulation.time:
                    # ADVANCE 0 -> no-op
                    continue
                self.advancing = True
                return
            
            elif block[0] == "SEIZE":
                # Use facility or enter delay chain if busy
                self.simulation.facilities[block[1][0]].seize(self)
            
            elif block[0] == "RELEASE":
                self.simulation.facilities[block[1][0]].release()
