from random import randint
from debug import debugmsg

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
    
    def update(self):
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
                self.simulation.queues[block[1][0]] += 1
            
            elif block[0] == "DEPART":
                self.simulation.queues[block[1][0]] -= 1
