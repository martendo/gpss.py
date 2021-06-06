class Facility:
    def __init__(self, name):
        self.name = name
        self.is_in_use = False
        self.entries = 0
    
    def seize(self):
        self.is_in_use = True
        self.entries += 1
    
    def release(self):
        self.is_in_use = False
