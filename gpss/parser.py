from .statement import Statement, StatementType
from .function import Function
from ._helpers import debugmsg, parser_error, warn

undefined = object()

OPERAND_LETTERS = ("A", "B", "C", "D", "E", "F", "G")
FUNCTION_TYPES = ("D",)

class Parser:
    def __init__(self):
        self.infile = None
    
    def __str__(self):
        return f"Parser({len(self.errors)})"
    
    def parse(self, infile=None, program=None):
        # Reset variables
        self.errors = []
        self.statements = []
        self.functions = []
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
        self.inputlines = tuple(map(
            self.remove_comment,
            self.inputdata.splitlines(),
        ))
        
        # Get Statements from program
        self.linenum = 1
        while self.linenum <= len(self.inputlines):
            line = self.inputlines[self.linenum - 1]
            
            # Empty, ignore
            if not line.strip():
                self.linenum += 1
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
                    f"(expected 1-3, got {len(fields)})")
                self.linenum += 1
                continue
            
            self.linenum += 1
    
    def remove_comment(self, line):
        # Semicolon comment
        commentpos = line.find(";")
        if commentpos != -1:
            return line[:commentpos]
        else:
            # Asterisk comment
            commentpos = line.find("*")
            if commentpos != -1:
                return line[:commentpos]
        # No comment
        return line
    
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
            self.operand_in(statement, 1, ("", "NP"))
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
            self.parse_transfer(statement)
        elif type_ is StatementType.FUNCTION:
            self.parse_function(statement)
        
        debugmsg("statement:", statement.type, statement.operands)
        
        self.statements.append(statement)
    
    def parse_transfer(self, statement):
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
                    parser_error(self, "A Operand of TRANSFER Block in "
                        "statistical transfer mode must be either a "
                        "fraction between 0 and .999+ or an integer "
                        "representing parts-per-thousand between 0 and "
                        f"999 (got \"{statement.operands[0]}\")")
    
    def parse_function(self, statement):
        function_type = statement.operands[1][0].upper()
        if function_type not in FUNCTION_TYPES:
            parser_error(self, "Unsupported Function type "
                f"\"{function_type}\" (must be one of " +
                str(FUNCTION_TYPES).replace("'", "") + ")")
        
        try:
            point_count = int(statement.operands[1][1:])
        except ValueError:
            parser_error(self, "Invalid number of points in Function "
                f"\"{statement.label}\" (got "
                f"\"{statement.operands[1][1:]}\")")
            return
        
        points = []
        while True:
            self.linenum += 1
            try:
                line = self.inputlines[self.linenum - 1]
            except IndexError:
                parser_error(self, "Unexpected end of file while "
                    "reading Function definition (expected "
                    f"{point_count} points, found {len(points)})")
                break
            
            for point in line.split("/"):
                values = point.split(",")
                point = []
                if len(values) != 2:
                    parser_error(self, f"Point {len(points) + 1} of "
                        f"Function \"{statement.label}\" " +
                        ("is missing" if len(values) < 2 else "has too many") + " "
                        f"values (expected 2, got {len(values)})")
                else:
                    for v, value in enumerate(values):
                        value = value.strip()
                        try:
                            point.append(float(value))
                        except ValueError:
                            parser_error(self,
                                ("X" if v == 0 else "Y") +
                                f"{len(points) + 1} value of Function "
                                f"\"{statement.label}\" is not a "
                                f"number (got \"{value}\")")
                points.append(point)
            
            if len(points) == point_count:
                break
            elif len(points) > point_count:
                parser_error(self, "Too many points given in Function "
                    f"\"{statement.label}\" (expected {point_count}, "
                    f"got {len(points)})")
        
        debugmsg("points:", points)
        
        self.functions.append(Function(
            function_type,
            statement.operands[0],
            points,
            statement.label,
        ))
    
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
