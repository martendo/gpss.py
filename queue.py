from error import EntityError

class Queue:
    def __init__(self, name):
        self.name = name
        self.content = 0
        self.entries = 0
        self.max = 0
    
    def enter(self, content):
        self.content += content
        if self.content > self.max:
            self.max = self.content
        self.entries += content
    
    def depart(self, content):
        self.content -= content
        if self.content < 0:
            raise EntityError("DEPART resulted in negative content in "
                f"Queue \"{self.name}\" ({self.content})")
