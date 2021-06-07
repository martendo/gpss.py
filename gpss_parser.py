from statements import Statements
from debug import debugmsg
from error import ParserError

class Parser:
    def __init__(self):
        self.statements = []
        self.storages = []
    
    def parse(self, inputfile):
        # Open and read GPSS program
        self.inputfile = inputfile
        with open(self.inputfile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = map(lambda line: line.strip(),
            self.inputdata.splitlines())
        
        # Get statements from program
        for linenum, line in enumerate(self.inputlines, 1):
            # Blank or comment line, ignore
            if line == "" or line[0] == "*" or line[0] == ";":
                continue
            
            # Remove any inline comments
            commentpos = line.find(";")
            if commentpos != -1:
                line = line[:commentpos]
            
            fields = line.split()
            debugmsg("fields:", fields)
            
            if len(fields) == 1:
                statement = Statement(linenum, fields[0])
            elif len(fields) == 2:
                if hasattr(Statements, fields[0].upper()) or "," in fields[1]:
                    # Statement and parameters
                    statement = Statement(linenum, fields[0], fields[1])
                else:
                    # Label and statement
                    statement = Statement(linenum, fields[1],
                        label=fields[0])
            elif len(fields) == 3:
                # Label, statement, and parameters
                statement = Statement(linenum, fields[1], fields[2],
                    label=fields[0])
            else:
                raise ParserError(linenum, "Too many fields in line "
                    f"(expected 1-3, got {len(fields)}):\n"
                    f"        \"{line.strip()}\"")
            debugmsg("statement:", statement.type, tuple(filter(bool,
                statement.parameters)), statement.label)
            
            self.statements.append(statement)
            
            # Save Storage definitions to later create them
            if statement.type == Statements.STORAGE:
                self.storages.append((statement.label, statement.parameters[0]))
                debugmsg("storage:", statement.label, statement.parameters[0])

class Statement:
    LETTERS = ("A", "B", "C", "D", "E", "F", "G")
    
    def __init__(self, linenum, name, parameters="", label=None):
        self.linenum = linenum
        self.name = name
        try:
            self.type = getattr(Statements, self.name.upper())
        except AttributeError:
            raise ParserError(self.linenum,
                f"Unsupported Statement \"{self.name}\"")
        self.parameters = parameters.split(",")
        if len(self.parameters) < len(self.LETTERS):
            self.parameters.extend([""] * (len(self.LETTERS) - len(self.parameters)))
        self.label = label
        
        if self.type == Statements.START:
            self.intifyparam(0, req=self.positive)
        elif self.type == Statements.GENERATE:
            self.intifyparam(0, 0, req=self.nonnegative)
            self.intifyparam(1, 0, req=self.nonnegative)
        elif self.type == Statements.TERMINATE:
            self.intifyparam(0, 0, req=self.nonnegative)
        elif self.type == Statements.ADVANCE:
            self.intifyparam(0, 0, req=self.nonnegative)
            self.intifyparam(1, 0, req=self.nonnegative)
        elif self.type in (Statements.QUEUE, Statements.DEPART):
            self.intifyparam(1, 1, req=self.positive)
        elif self.type in (Statements.ENTER, Statements.LEAVE):
            self.intifyparam(1, 1, req=self.positive)
        elif self.type == Statements.STORAGE:
            self.intifyparam(0, req=self.positive)
    
    def positive(self, index):
        if self.parameters[index] <= 0:
            raise ParserError(self.linenum,
                f"Parameter {self.LETTERS[index]} of "
                f"{self.name} must be a strictly positive integer "
                f"(got \"{self.parameters[index]}\")")
    
    def nonnegative(self, index):
        if self.parameters[index] < 0:
            raise ParserError(self.linenum,
                f"Parameter {self.LETTERS[index]} of "
                f"{self.name} must be a non-negative integer "
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
            raise ParserError(self.linenum,
                f"Parameter {self.LETTERS[index]} of "
                f"{self.name} must be an integer "
                f"(got \"{self.parameters[index]}\")")
        
        if req is not None:
            req(index)
