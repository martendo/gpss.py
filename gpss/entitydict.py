from collections import defaultdict

class entitydict(defaultdict):
    def __init__(self, simulation, *args, **kwargs):
        self.simulation = simulation
        super().__init__(*args, **kwargs)
    
    def __missing__(self, key):
        item = self[key] = self.default_factory(self.simulation, key)
        return item
