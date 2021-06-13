from .error import simulation_error, warn

class Queue:
    def __init__(self, simulation, name):
        self.simulation = simulation
        self.name = name
        
        self.content = 0
        self.transactions = {}
        self.reset()
    
    def reset(self):
        self.entries = 0
        self.max_content = 0
        self.utilization = 0
        self.zero_entries = 0
        self.last_change = self.simulation.time
    
    def __repr__(self):
        return f"Queue({self.content})"
    
    def change(self):
        self.utilization += (
            (self.simulation.time - self.last_change) * self.content)
        self.last_change = self.simulation.time
    
    def join(self, transaction, content):
        self.change()
        self.content += content
        if self.content > self.max_content:
            self.max_content = self.content
        self.entries += content
        self.transactions[transaction] = self.simulation.time
    
    def depart(self, transaction, content):
        self.change()
        self.content -= content
        if self.content < 0:
            simulation_error(self.simulation.parser.infile,
                transaction.current_linenum,
                "DEPART resulted in negative content in Queue "
                f"\"{self.name}\" ({self.content})")
        try:
            if self.transactions[transaction] == self.simulation.time:
                self.zero_entries += content
        except KeyError:
            warn(self.simulation.parser.infile,
                transaction.current_linenum, "Transaction DEPARTed "
                f"Queue \"{self.name}\" without first joining it")
