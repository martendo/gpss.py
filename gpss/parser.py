from .statement import Statement, StatementType
from .debug import debugmsg
from .error import parser_error, warn

undefined = object()

OPERAND_LETTERS = ("A", "B", "C", "D", "E", "F", "G")

class Parser:
    def __init__(self):
        self.error_count = 0
        
        self.statements = []
        self.storages = []
        self.current_label = None
        self.labels = {}
    
    def parse(self, infile):
        # Open and read GPSS program
        self.infile = infile
        with open(self.infile, "r") as file:
            self.inputdata = file.read()
        self.inputlines = map(lambda line: line.strip(),
            self.inputdata.splitlines())
        
        # Get statements from program
        for linenum, line in enumerate(self.inputlines, 1):
            self.linenum = linenum
            
            # Remove any inline comments
            commentpos = line.find(";")
            if commentpos != -1:
                line = line[:commentpos]
            else:
                commentpos = line.find("*")
                if commentpos != -1:
                    line = line[:commentpos]
            
            # Empty, ignore
            if not line.strip():
                continue
            
            fields = line.split()
            debugmsg("fields:", fields)
            
            if len(fields) == 1:
                if fields[0][-1] == ":":
                    # Label
                    self.current_label = fields[0][:-1]
                else:
                    # Statement
                    self.parse_statement(fields[0])
            elif len(fields) == 2:
                if hasattr(StatementType, fields[0].upper()) or "," in fields[1]:
                    # Statement and operands
                    self.parse_statement(fields[0], fields[1])
                else:
                    # Label and statement
                    self.parse_statement(fields[1], label=fields[0])
            elif len(fields) == 3:
                # Label, statement, and operands
                self.parse_statement(fields[1], fields[2],
                    label=fields[0])
            else:
                parser_error(self, "Too many fields in line "
                    f"(expected 1-3, got {len(fields)}): "
                    f"\"{line.strip()}\"")
                continue
    
    def parse_statement(self, name, operands="", label=None):
        # Find Statement type
        try:
            type_ = StatementType[name.upper()]
        except KeyError:
            parser_error(self, f"Unsupported Statement \"{name}\"")
            return
        
        # Get Operands
        operands = operands.split(",")
        if len(operands) < len(OPERAND_LETTERS):
            operands.extend([""] * (len(OPERAND_LETTERS) - len(operands)))
        
        # Get label
        if label is None and self.current_label is not None:
            # Label defined previously
            label = self.current_label
            # Label has gone to this Statement -> don't give it to
            # another
            self.current_label = None
        
        # Create Statement object
        statement = Statement(type_, name, operands, self.linenum,
            len(self.statements))
        
        # Store a reference to this Statement
        if label is not None:
            if label not in self.labels:
                self.labels[label] = statement
            else:
                warn(self.infile, self.linenum,
                    f"Label \"{label}\" already defined at line "
                    + str(self.labels[label].linenum))
        
        # Parse necessary Operands
        if type_ == StatementType.START:
            self.parse_operand(statement, 0, req=self.positive)
        elif type_ == StatementType.GENERATE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
            self.parse_operand(statement, 1, 0, req=self.nonnegative)
            self.parse_operand(statement, 2, None, req=self.nonnegative)
            self.parse_operand(statement, 3, None, req=self.positive)
            self.parse_operand(statement, 4, 0, req=self.nonnegative)
        elif type_ == StatementType.TERMINATE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
        elif type_ == StatementType.ADVANCE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
            self.parse_operand(statement, 1, 0, req=self.nonnegative)
        elif type_ in (StatementType.QUEUE, StatementType.DEPART):
            self.nonempty(statement, 0)
            self.parse_operand(statement, 1, 1, req=self.positive)
        elif type_ in (StatementType.SEIZE, StatementType.RELEASE):
            self.nonempty(statement, 0)
        elif type_ in (StatementType.ENTER, StatementType.LEAVE):
            self.parse_operand(statement, 1, 1, req=self.positive)
        elif type_ == StatementType.STORAGE:
            self.parse_operand(statement, 0, req=self.positive)
        
        debugmsg("statement:", statement.type, statement.operands)
        
        # Save Storage definitions to later create them
        if type_ == StatementType.STORAGE:
            self.storages.append((label, statement.operands[0]))
            debugmsg("storage:", label, statement.operands[0])
        
        self.statements.append(statement)
        
        return True
    
    def parse_operand(self, statement, index, default=undefined,
            req=None):
        try:
            if default is not undefined:
                statement.operands[index] = (
                    default if not statement.operands[index]
                    else int(statement.operands[index]))
            else:
                statement.operands[index] = int(statement.operands[index])
        except ValueError:
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be an integer "
                f"(got \"{statement.operands[index]}\")")
            return
        
        if req is not None:
            req(statement, index)
    
    # Error if operand is not strictly positive
    def positive(self, statement, index):
        if (statement.operands[index] is not None
                and statement.operands[index] <= 0):
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be a strictly positive integer "
                f"(got \"{statement.operands[index]}\")")
    
    # Error if operand is negative
    def nonnegative(self, statement, index):
        if (statement.operands[index] is not None
                and statement.operands[index] < 0):
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be a non-negative integer "
                f"(got \"{statement.operands[index]}\")")
    
    # Error if operand is empty string
    def nonempty(self, statement, index):
        if statement.operands[index] == "":
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must not be empty")
