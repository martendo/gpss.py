from error import EntityError

class Queue:
    def __init__(self, name):
        self.name = name
        self.content = 0
        self.max = 0
    
    def enter(self):
        self.content += 1
        if self.content > self.max:
            self.max = self.content
    
    def depart(self):
        self.content -= 1
        if self.content < 0:
            raise EntityError("DEPART resulted in negative content in "
                f"Queue \"{self.name}\" ({self.content})")
