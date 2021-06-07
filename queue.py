from error import EntityError

class Queue:
    def __init__(self, name):
        self.name = name
        self.contents = 0
        self.max = 0
    
    def enter(self):
        self.contents += 1
        if self.contents > self.max:
            self.max = self.contents
    
    def depart(self):
        self.contents -= 1
        if self.contents < 0:
            raise EntityError("DEPART resulted in negative contents in "
                f"Queue {self.name} ({self.contents})")
