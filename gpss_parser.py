from debug import debugmsg

class Parser:
    def __init__(self):
        self.statements = []
        self.queues = []
    
    def open(self, inputfile):
        self.inputfile = inputfile
        with open(inputfile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = self.inputdata.split("\n")
    
    def parse(self):
        for line in self.inputlines:
            # Comment line
            if line[0] == "*":
                continue
            
            statement = line[7:18].strip()
            parameters = line[18:].strip().split(",")
            debugmsg("statement:", statement, parameters)
            
            self.statements.append((statement, parameters))
            
            # Save queues' names to later create them
            if statement in ("QUEUE", "DEPART"):
                self.queues.append(parameters[0])
                debugmsg("queue:", parameters[0])
