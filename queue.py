class Queue:
    def __init__(self):
        self.contents = 0
        self.max = 0
    
    def enter(self):
        self.contents += 1
        if self.contents > self.max:
            self.max = self.contents
    
    def leave(self):
        self.contents -= 1
