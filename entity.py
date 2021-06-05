from random import randint
from debug import debugmsg

class Entity:
    def __init__(self, simulation, parameters):
        self.simulation = simulation
        self.parameters = parameters
        self.program = []
    
    def update_nexttime(self):
        # Default spread modifier to 0
        try:
            spread = int(self.parameters[1])
        except IndexError:
            spread = 0
        # Set next generation time value
        self.nexttime = randint(
            self.simulation.time + (int(self.parameters[0]) - spread),
            self.simulation.time + (int(self.parameters[0]) + spread),
        )

class EntityInstance:
    def __init__(self, entity):
        self.entity = entity
        self.simulation = self.entity.simulation
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
            block = self.entity.program[self.currentcard]
            self.currentcard += 1
            if block[0] == "TERMINATE":
                # Update remaining transactions count
                try:
                    self.simulation.transactions -= int(block[1][0])
                except ValueError:
                    pass
                # Destroy this transaction
                self.simulation.entityinsts.remove(self)
                return
            elif block[0] == "QUEUE":
                self.queue = block[1][0]
                queue = self.simulation.queues[self.queue]
                queuelen = len(queue)
                queue.append(self)
                if queuelen > 0:
                    # Need to wait in the queue
                    return
