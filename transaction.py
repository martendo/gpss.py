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
        self.nexttime = randint(
            self.simulation.time + (self.interval - self.spread),
            self.simulation.time + (self.interval + self.spread),
        )
    
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
        self.queue = None
    
    def update(self):
        if self.queue is not None:
            # Waiting in a queue
            if self.simulation.queues[self.queue].index(self) == 0:
                # At the front of the queue, stop waiting
                self.queue = None
            else:
                # Keep waiting -> do nothing
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
                self.queue = block[1][0]
                queue = self.simulation.queues[self.queue]
                queuelen = len(queue)
                queue.append(self)
                if queuelen > 0:
                    # Need to wait in the queue
                    return
