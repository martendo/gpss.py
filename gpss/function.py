class Function:
    def __init__(self, type_, arg, points, name):
        self.type = type_
        self.arg = arg
        self.points = points
        self.name = name
    
    def __str__(self):
        return f"Function({self.arg}, {self.type}{len(self.points)})"
    
    def __call__(self):
        raise NotImplementedError
