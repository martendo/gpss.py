from error import EntityError

class Queue:
    def __init__(self, name):
        self.name = name
        self.content = 0
        self.entries = 0
        self.max = 0
        self.zero_entries = 0
        self.transactions = {}
    
    def enter(self, transaction, content):
        self.content += content
        if self.content > self.max:
            self.max = self.content
        self.entries += content
        self.transactions[transaction] = transaction.simulation.time
    
    def depart(self, transaction, content):
        self.content -= content
        if self.content < 0:
            raise EntityError("DEPART resulted in negative content in "
                f"Queue \"{self.name}\" ({self.content})")
        if self.transactions[transaction] == transaction.simulation.time:
            self.zero_entries += content
