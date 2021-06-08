from .error import simulation_error, warn

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
    
    def join(self, transaction, content):
        self.content += content
        if self.content > self.max:
            self.max = self.content
        self.entries += content
        self.transactions[transaction] = self.simulation.time
        self.change()
    
    def depart(self, transaction, content):
        self.content -= content
        if self.content < 0:
            simulation_error(self.simulation.parser.inputfile,
                transaction.current_linenum,
                "DEPART resulted in negative content in Queue "
                f"\"{self.name}\" ({self.content})")
        try:
            if self.transactions[transaction] == self.simulation.time:
                self.zero_entries += content
        except KeyError:
            warn(self.simulation.parser.inputfile,
                transaction.current_linenum, "Transaction DEPARTed "
                f"Queue \"{self.name}\" without first joining it")
        self.change()
