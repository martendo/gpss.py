from collections import deque
from entity import Entity, EntityInstance
from debug import debugmsg

class Simulation:
    def __init__(self):
        self.simulate = False
        self.running = False
        self.entities = set()
        self.entityinsts = set()
        self.queues = {}
        self.time = 0
    
    def run(self, parser):
        self.program = parser.statements
        # Create queues used in simulation
        for queue in parser.queues:
            self.queues[queue] = deque()
        
        i = 0
        while i < len(self.program):
            statement = self.program[i]
            i += 1
            if statement[0] == "SIMULATE":
                # Run the simulation
                self.simulate = True
            elif statement[0] == "GENERATE":
                # Define an entity
                debugmsg("entity:", statement)
                entity = Entity(self, statement[1])
                j = i
                while True:
                    # Get entity's program
                    block = self.program[j]
                    j += 1
                    entity.program.append(block)
                    if block[0] == "TERMINATE":
                        # Entity's program ends at TERMINATE
                        break
                self.entities.add(entity)
                i = j
            elif statement[0] == "START":
                # Set number of transactions to complete
                self.transactions = int(statement[1][0])
                debugmsg("transactions:", self.transactions)
        
        # Set initial entity instance generation times
        for entity in self.entities:
            entity.update_nexttime()
        
        # Start the simulation
        self.running = True
        while self.running:
            self.advance()
    
    def advance(self):
        for entity in self.entities:
            if self.time == entity.nexttime:
                # Generate a new entity instance
                debugmsg("generate:", self.time, entity.parameters)
                entityinst = EntityInstance(entity)
                self.entityinsts.add(entityinst)
                # Update next entity instance generation time
                entity.update_nexttime()
        
        # Run entity instance programs
        for entityinst in tuple(self.entityinsts):
            entityinst.update()
            # Completed all transactions, stop running
            if self.transactions < 1:
                self.running = False
                break
        
        # Move through time
        self.time += 1
