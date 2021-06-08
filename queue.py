from error import SimulationError

class Queue:
    def __init__(self, simulation, name):
        self.simulation = simulation
        self.name = name
        
        self.content = 0
        self.entries = 0
        self.max = 0
        self.zero_entries = 0
        self.transactions = {}
        
        self.changes = []
    
    def change(self):
        self.changes.append((self.content, self.simulation.time))
    
    def enter(self, transaction, content):
        self.content += content
        if self.content > self.max:
            self.max = self.content
        self.entries += content
        self.transactions[transaction] = self.simulation.time
        self.change()
    
    def depart(self, transaction, content):
        self.content -= content
        if self.content < 0:
            raise SimulationError(transaction.current_linenum,
                "DEPART resulted in negative content in Queue "
                f"\"{self.name}\" ({self.content})")
        if self.transactions[transaction] == self.simulation.time:
            self.zero_entries += content
        self.change()
