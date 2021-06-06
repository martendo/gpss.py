from debug import debugmsg
from error import ParserError

class Parser:
    def __init__(self):
        self.statements = []
        self.queues = []
        self.facilities = []
    
    def parse(self, inputfile):
        # Open and read GPSS program
        self.inputfile = inputfile
        with open(self.inputfile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = self.inputdata.split("\n")
        
        # Get statements from program
        for line in self.inputlines:
            # Blank or Comment line, ignore
            if line.strip() == "" or line[0] == "*":
                continue
            
            statement = Statement(line[7:18].strip(),
                line[18:].strip().split(","))
            debugmsg("statement:", statement.type, statement.parameters)
            
            self.statements.append(statement)
            
            # Save queues' and facilities' names to later create them
            if statement.type in ("QUEUE", "DEPART"):
                self.queues.append(statement.parameters[0])
                debugmsg("queue:", statement.parameters[0])
            elif statement.type in ("SEIZE", "RELEASE"):
                self.facilities.append(statement.parameters[0])
                debugmsg("facility:", statement.parameters[0])

class Statement:
    LETTERS = ("A", "B", "C", "D", "E", "F", "G")
    
    def __init__(self, type_, parameters):
        self.type = type_
        self.parameters = parameters
        if len(self.parameters) < len(self.LETTERS):
            self.parameters.extend([""] * (len(self.LETTERS) - len(self.parameters)))
        
        if self.type == "START":
            self.intifyparam(0, req=self.positive)
        elif self.type == "GENERATE":
            self.intifyparam(0, 0, req=self.nonnegative)
            self.intifyparam(1, 0, req=self.nonnegative)
        elif self.type == "TERMINATE":
            self.intifyparam(0, 0, req=self.nonnegative)
        elif self.type == "ADVANCE":
            self.intifyparam(0, 0, req=self.nonnegative)
            self.intifyparam(1, 0, req=self.nonnegative)
    
    def positive(self, index):
        if self.parameters[index] <= 0:
            raise ParserError(f"Parameter {self.LETTERS[index]} of "
                f"{self.type} must be a strictly positive integer "
                f"(got \"{self.parameters[index]}\")")
    
    def nonnegative(self, index):
        if self.parameters[index] < 0:
            raise ParserError(f"Parameter {self.LETTERS[index]} of "
                f"{self.type} must be a non-negative integer "
                f"(got \"{self.parameters[index]}\")")
    
    def intifyparam(self, index, default=None, req=None):
        try:
            if default is not None:
                self.parameters[index] = (
                    default if self.parameters[index] == ""
                    else int(self.parameters[index]))
            else:
                self.parameters[index] = int(self.parameters[index])
        except ValueError:
            raise ParserError(f"Parameter {self.LETTERS[index]} of "
                f"{self.type} must be an integer "
                f"(got \"{self.parameters[index]}\")")
        
        if req is not None:
            req(index)
