from .statement import Statement, StatementType
from .function import Function
from ._helpers import debugmsg, parser_error, warn

undefined = object()

OPORD = 0x41 # ord("A")
MAX_OPERAND_COUNT = 7
FUNCTION_TYPES = ("D",)

class Parser:
	def __init__(self):
		self.infile = None
		self.errors = []

	def __str__(self):
		if self.infile is not None:
			filename = f"\"{self.infile}\""
		else:
			filename = "<instr>"
		s = f"Parser: file {filename} ({len(self.errors)} error"
		if len(self.errors) != 1:
			s += "s"
		s += ")"
		return s

	def parse(self, infile=None, program=None):
		# Reset variables
		self.errors = []
		self.statements = []
		self.snamap = {
			"FN": {},
		}
		self.current_label = None
		self.labels = {}

		# Open and read GPSS program
		self.infile = infile
		if self.infile is not None:
			with open(self.infile, "r") as file:
				self.inputdata = file.read()
		else:
			self.inputdata = program
		self.inputlines = tuple(map(self.remove_comment, self.inputdata.splitlines()))

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
				self.parse_statement(fields[1], fields[2], label=fields[0])
			else:
				parser_error(self, f"Too many fields in line (expected 1-3, got {len(fields)})")
				self.linenum += 1
				continue

			self.linenum += 1

	def remove_comment(self, line):
		semipos = line.find(";")
		astpos = line.find("*")
		# No comment
		if semipos == -1 and astpos == -1:
			return line
		# Remove comment: first '*' or ';' to end of line
		if semipos != -1 and astpos == -1:
			return line[:semipos]
		elif astpos != -1 and semipos == -1:
			return line[:astpos]
		else:
			return line[:min(semipos, astpos)]

	def parse_statement(self, name, operands="", label=None):
		# Find Statement type
		try:
			type_ = StatementType[name.upper()]
		except KeyError:
			parser_error(self, f"Unsupported Statement \"{name}\"")
			return

		# Get Operands
		operands = operands.split(",")
		if len(operands) < MAX_OPERAND_COUNT:
			operands.extend([""] * (MAX_OPERAND_COUNT - len(operands)))

		# Get label
		if label is not None and label[-1] == ":":
			label = label[:-1]
		if label is None and self.current_label is not None:
			# Label defined previously
			label = self.current_label
			# Label has gone to this Statement -> don't give it to another
			self.current_label = None

		# Create Statement object
		statement = Statement(type_, name, operands, label, self.linenum, len(self.statements))

		# Store a reference to this Statement
		if label is not None:
			if label not in self.labels:
				self.labels[label] = statement
			else:
				warn(self.infile, self.linenum,
					f"Label \"{label}\" already defined at line {self.labels[label].linenum}")

		# Parse necessary Operands
		if type_ is StatementType.START:
			self.parse_operand(statement, 0, req=self.positive)
			self.operand_in(statement, 1, ("", "NP"))
			self.parse_operand(statement, 2, None, req=self.positive)
		elif type_ is StatementType.GENERATE:
			self.parse_operand(statement, 0, 0, req=self.nonnegative, sna_classes=("FN",))
			self.parse_operand(statement, 1, 0, req=self.nonnegative, sna_classes=("FN",))
			self.parse_operand(statement, 2, None, req=self.nonnegative)
			self.parse_operand(statement, 3, None, req=self.positive)
			self.parse_operand(statement, 4, 0, req=self.nonnegative)
		elif type_ is StatementType.TERMINATE:
			self.parse_operand(statement, 0, 0, req=self.nonnegative)
		elif type_ is StatementType.ADVANCE:
			self.parse_operand(statement, 0, 0, req=self.nonnegative, sna_classes=("FN",))
			self.parse_operand(statement, 1, 0, req=self.nonnegative, sna_classes=("FN",))
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
					parser_error(self, "A Operand of TRANSFER Block in statistical transfer mode must be either "
						"a fraction between 0 and .999+ or an integer representing parts-per-thousand between 0 and 999 "
						f"(got \"{statement.operands[0]}\")")

	def parse_function(self, statement):
		rn = None
		try:
			if statement.operands[0][:2] != "RN":
				raise ValueError
			rn = int(statement.operands[0][2:])
		except ValueError:
			parser_error(self, f"Argument of Function must be a random number generator (got \"{statement.operands[0]}\")")

		function_type = statement.operands[1][0].upper()
		if function_type not in FUNCTION_TYPES:
			parser_error(self, f"Unsupported Function type \"{function_type}\" (must be one of "
				+ str(FUNCTION_TYPES).replace("'", "") + ")")

		try:
			point_count = int(statement.operands[1][1:])
		except ValueError:
			parser_error(self, f"Invalid number of points in Function \"{statement.label}\" "
				f"(got \"{statement.operands[1][1:]}\")")
			return

		points = []
		while True:
			self.linenum += 1
			try:
				line = self.inputlines[self.linenum - 1]
			except IndexError:
				parser_error(self, "Unexpected end of file while reading Function definition "
					f"(expected {point_count} points, found {len(points)})")
				break

			for point in line.split("/"):
				if not point:
					parser_error(self, f"Point {len(points) + 1} of Function \"{statement.label}\" is empty")
				values = point.split(",")
				point = [None, None]
				if len(values) != 2:
					parser_error(self, f"Point {len(points) + 1} of Function \"{statement.label}\" "
						+ ("is missing" if len(values) < 2 else "has too many") + f" values (expected 2, got {len(values)})")
				for i in range(min(2, len(values))):
					value = values[i].strip()
					valuestr = ("X" if i == 0 else "Y") + f"{len(points) + 1} value of Function \"{statement.label}\""
					if not value:
						parser_error(self, f"{valuestr} is empty")
						continue
					try:
						point[i] = float(value)
					except ValueError:
						parser_error(self, f"{valuestr} is not a number (got \"{value}\")")
				points.append(point)

			if len(points) == point_count:
				break
			elif len(points) > point_count:
				parser_error(self, f"Too many points given in Function \"{statement.label}\" "
					f"(expected {point_count}, got {len(points)})")
				break

		debugmsg("points:", points)

		self.snamap["FN"][statement.label] = Function(
			function_type,
			rn,
			points,
			statement.label,
		)

	def parse_operand(self, statement, index, default=undefined, req=None, sna_classes=()):
		try:
			if default is not undefined:
				statement.operands[index] = default if not statement.operands[index] else int(statement.operands[index])
			else:
				statement.operands[index] = int(statement.operands[index])
		except ValueError:
			# Not an integer, check for allowed SNAs
			for sna_class in sna_classes:
				prefix = statement.operands[index][:len(sna_class) + 1].upper()
				if prefix != f"{sna_class}$":
					continue
				# Operand is a valid SNA, get entity
				sna = statement.operands[index][len(sna_class) + 1:]
				try:
					statement.operands[index] = self.snamap[sna_class][sna]
				except KeyError:
					parser_error(self, f"Entity \"{statement.operands[index]}\" is not defined")
				# Return; don't check if SNA meets requirements
				return
			else:
				# Not an integer and not an allowed SNA
				parser_error(self, f"{chr(index + OPORD)} Operand of {statement.name} must be an integer "
					+ (f"or SNA of type " + str(sna_classes).replace("'", "\"") + " " if len(sna_classes) else "")
					+ f"(got \"{statement.operands[index]}\")")
				return

		if req is not None:
			req(statement, index)

	# Error if Operand is not strictly positive
	def positive(self, statement, index):
		if statement.operands[index] is not None and statement.operands[index] <= 0:
			parser_error(self, f"{chr(index + OPORD)} Operand of {statement.name} must be a strictly positive integer "
				f"(got \"{statement.operands[index]}\")")

	# Error if Operand is negative
	def nonnegative(self, statement, index):
		if statement.operands[index] is not None and statement.operands[index] < 0:
			parser_error(self, f"{chr(index + OPORD)} Operand of {statement.name} must be a non-negative integer "
				f"(got \"{statement.operands[index]}\")")

	# Error if Operand is empty string
	def nonempty(self, statement, index):
		if statement.operands[index] == "":
			parser_error(self, f"{chr(index + OPORD)} Operand of {statement.name} must not be empty")

	# Error if Operand is not in a set of allowed values
	def operand_in(self, statement, index, allowed):
		statement.operands[index] = statement.operands[index].upper()
		if statement.operands[index] not in allowed:
			parser_error(self, f"{chr(index + OPORD)} Operand of {statement.name} must be one of "
				+ str(allowed).replace("''", "empty").replace("'", "\""))
