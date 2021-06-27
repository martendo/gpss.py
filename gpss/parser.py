from .statement import Statement, StatementType
from ._helpers import debugmsg, parser_error, warn

undefined = object()

OPERAND_LETTERS = ("A", "B", "C", "D", "E", "F", "G")

class Parser:
    def __init__(self):
        self.infile = None
    
    def __str__(self):
        return f"Parser({len(self.errors)})"
    
    def parse(self, infile=None, program=None):
        # Reset variables
        self.errors = []
        self.statements = []
        self.current_label = None
        self.labels = {}
        
        # Open and read GPSS program
        if infile is not None:
            self.infile = infile
            with open(self.infile, "r") as file:
                self.inputdata = file.read()
        else:
            self.inputdata = program
            self.infile = "instr"
        self.inputlines = map(str.strip, self.inputdata.splitlines())
        
        # Get Statements from program
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
                    # Statement and Operands
                    self.parse_statement(fields[0], fields[1])
                else:
                    # Label and Statement
                    self.parse_statement(fields[1], label=fields[0])
            elif len(fields) == 3:
                # Label, Statement, and Operands
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
        statement = Statement(type_, name, operands, label,
            self.linenum, len(self.statements))
        
        # Store a reference to this Statement
        if label is not None:
            if label not in self.labels:
                self.labels[label] = statement
            else:
                warn(self.infile, self.linenum,
                    f"Label \"{label}\" already defined at line "
                    + str(self.labels[label].linenum))
        
        # Parse necessary Operands
        if type_ is StatementType.START:
            self.parse_operand(statement, 0, req=self.positive)
            self.operand_in(statement, 1, ["", "NP"])
            self.parse_operand(statement, 2, None, req=self.positive)
        elif type_ is StatementType.GENERATE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
            self.parse_operand(statement, 1, 0, req=self.nonnegative)
            self.parse_operand(statement, 2, None, req=self.nonnegative)
            self.parse_operand(statement, 3, None, req=self.positive)
            self.parse_operand(statement, 4, 0, req=self.nonnegative)
        elif type_ is StatementType.TERMINATE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
        elif type_ is StatementType.ADVANCE:
            self.parse_operand(statement, 0, 0, req=self.nonnegative)
            self.parse_operand(statement, 1, 0, req=self.nonnegative)
        elif type_ in (StatementType.QUEUE, StatementType.DEPART):
            self.nonempty(statement, 0)
            self.parse_operand(statement, 1, 1, req=self.positive)
        elif type_ in (StatementType.SEIZE, StatementType.RELEASE):
            self.nonempty(statement, 0)
        elif type_ in (StatementType.ENTER, StatementType.LEAVE):
            self.parse_operand(statement, 1, 1, req=self.positive)
        elif type_ is StatementType.STORAGE:
            self.parse_operand(statement, 0, req=self.positive)
        elif type_ is StatementType.TRANSFER:
            if statement.operands[0] == "":
                # Unconditional transfer mode
                statement.operands[0] = None
            
            elif statement.operands[0] == "BOTH":
                # BOTH mode
                pass
            
            else:
                # Statistical transfer mode
                try:
                    chance = int(statement.operands[0])
                    if not(0 <= chance < 1000):
                        raise ValueError
                    statement.operands[0] = chance / 1000
                except ValueError:
                    try:
                        chance = float(statement.operands[0])
                        if not(0 <= chance < 1):
                            raise ValueError
                        statement.operands[0] = chance
                    except ValueError:
                        parser_error(self, "A Operand of TRANSFER "
                            "Block in statistical transfer mode must "
                            "be either a fraction between 0 and .999+ "
                            "or an integer representing parts-per-"
                            "thousand between 0 and 999 "
                            f"(got \"{statement.operands[0]}\")")
        
        debugmsg("statement:", statement.type, statement.operands)
        
        self.statements.append(statement)
    
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
    
    # Error if Operand is not strictly positive
    def positive(self, statement, index):
        if (statement.operands[index] is not None
                and statement.operands[index] <= 0):
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be a strictly positive integer "
                f"(got \"{statement.operands[index]}\")")
    
    # Error if Operand is negative
    def nonnegative(self, statement, index):
        if (statement.operands[index] is not None
                and statement.operands[index] < 0):
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be a non-negative integer "
                f"(got \"{statement.operands[index]}\")")
    
    # Error if Operand is empty string
    def nonempty(self, statement, index):
        if statement.operands[index] == "":
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must not be empty")
    
    # Error if Operand is not in a set of allowed values
    def operand_in(self, statement, index, allowed):
        statement.operands[index] = statement.operands[index].upper()
        if statement.operands[index] not in allowed:
            parser_error(self, OPERAND_LETTERS[index] + " Operand of "
                f"{statement.name} must be one of "
                + str(allowed).replace("''", "empty").replace("'", "\""))
