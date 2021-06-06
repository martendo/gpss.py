from debug import debugmsg

class Parser:
    def __init__(self):
        self.statements = []
        self.queues = []
        self.facilities = []
    
    def parse(self, inputfile):
        # Read GPSS program
        self.inputfile = inputfile
        with open(self.inputfile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = self.inputdata.split("\n")
        
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
            elif statement in ("SEIZE", "RELEASE"):
                self.facilities.append(parameters[0])
                debugmsg("facility:", parameters[0])
