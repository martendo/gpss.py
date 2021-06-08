from statements import Statements
from debug import debugmsg
from error import parser_error

undefined = object()

class Parser:
    def __init__(self):
        self.error_count = 0
        
        self.statements = []
        self.storages = []
        self.current_label = None
        self.found_simulate = False
    
    def parse(self, inputfile):
        # Open and read GPSS program
        self.inputfile = inputfile
        with open(self.inputfile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = map(lambda line: line.strip(),
            self.inputdata.splitlines())
        
        # Get statements from program
        for linenum, line in enumerate(self.inputlines, 1):
            self.linenum = linenum
            
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
                if fields[0][-1] == ":":
                    # Label
                    self.current_label = fields[0][:-1]
                else:
                    # Statement
                    statement = Statement(self, fields[0])
            elif len(fields) == 2:
                if hasattr(Statements, fields[0].upper()) or "," in fields[1]:
                    # Statement and operands
                    statement = Statement(self, fields[0], fields[1])
                else:
                    # Label and statement
                    statement = Statement(self, fields[1],
                        label=fields[0])
            elif len(fields) == 3:
                # Label, statement, and operands
                statement = Statement(self, fields[1], fields[2],
                    label=fields[0])
            else:
                parser_error(self.inputfile, linenum,
                    "Too many fields in line "
                    f"(expected 1-3, got {len(fields)}): "
                    f"\"{line.strip()}\"")
                self.error_count += 1
                continue
            
            if statement.error:
                # There was an error when creating this Statement
                # object, and it is completely unusable (e.g.
                # non-existent statement)
                continue
            debugmsg("statement:", statement.type, statement.operands,
                statement.label)
            
            self.statements.append(statement)
            
            # Save Storage definitions to later create them
            if statement.type == Statements.STORAGE:
                self.storages.append((statement.label, statement.operands[0]))
                debugmsg("storage:", statement.label, statement.operands[0])
            elif statement.type == Statements.SIMULATE:
                self.found_simulate = True

class Statement:
    LETTERS = ("A", "B", "C", "D", "E", "F", "G")
    
    def __init__(self, parser, name, operands="", label=None):
        self.parser = parser
        self.linenum = self.parser.linenum
        self.error = False
        
        # Find Statement type
        self.name = name
        try:
            self.type = getattr(Statements, self.name.upper())
        except AttributeError:
            parser_error(self.parser.inputfile, self.linenum,
                f"Unsupported Statement \"{self.name}\"")
            self.parser.error_count += 1
            self.error = True
            return
        
        # Get Operands
        self.operands = operands.split(",")
        if len(self.operands) < len(self.LETTERS):
            self.operands.extend([""] * (len(self.LETTERS) - len(self.operands)))
        
        # Get label
        if label is not None:
            self.label = label
        else:
            self.label = self.parser.current_label
            # Label goes to this Statement -> don't give it to another
            if self.label is not None:
                self.parser.current_label = None
        
        # Parse necessary Operands
        if self.type == Statements.START:
            self.intify_operand(0, req=self.positive)
        elif self.type == Statements.GENERATE:
            self.intify_operand(0, 0, req=self.nonnegative)
            self.intify_operand(1, 0, req=self.nonnegative)
            self.intify_operand(2, None, req=self.nonnegative)
            self.intify_operand(3, None, req=self.positive)
            self.intify_operand(4, 0, req=self.nonnegative)
        elif self.type == Statements.TERMINATE:
            self.intify_operand(0, 0, req=self.nonnegative)
        elif self.type == Statements.ADVANCE:
            self.intify_operand(0, 0, req=self.nonnegative)
            self.intify_operand(1, 0, req=self.nonnegative)
        elif self.type in (Statements.QUEUE, Statements.DEPART):
            self.nonempty(0)
            self.intify_operand(1, 1, req=self.positive)
        elif self.type in (Statements.SEIZE, Statements.RELEASE):
            self.nonempty(0)
        elif self.type in (Statements.ENTER, Statements.LEAVE):
            self.intify_operand(1, 1, req=self.positive)
        elif self.type == Statements.STORAGE:
            self.intify_operand(0, req=self.positive)
    
    def positive(self, index):
        if (self.operands[index] is not None
                and self.operands[index] <= 0):
            parser_error(self.parser.inputfile, self.linenum,
                f"{self.LETTERS[index]} Operand of {self.name} "
                "must be a strictly positive integer "
                f"(got \"{self.operands[index]}\")")
            self.parser.error_count += 1
    
    def nonnegative(self, index):
        if (self.operands[index] is not None
                and self.operands[index] < 0):
            parser_error(self.parser.inputfile, self.linenum,
                f"{self.LETTERS[index]} Operand of {self.name} "
                "must be a non-negative integer "
                f"(got \"{self.operands[index]}\")")
            self.parser.error_count += 1
    
    def nonempty(self, index):
        if self.operands[index] == "":
            parser_error(self.parser.inputfile, self.linenum,
                f"{self.LETTERS[index]} Operand of {self.name} "
                f"must not be empty")
            self.parser.error_count += 1
    
    def intify_operand(self, index, default=undefined, req=None):
        try:
            if default is not undefined:
                self.operands[index] = (
                    default if self.operands[index] == ""
                    else int(self.operands[index]))
            else:
                self.operands[index] = int(self.operands[index])
        except ValueError:
            parser_error(self.parser.inputfile, self.linenum,
                f"{self.LETTERS[index]} Operand of {self.name} "
                f"must be an integer (got \"{self.operands[index]}\")")
            self.parser.error_count += 1
            return
        
        if req is not None:
            req(index)
