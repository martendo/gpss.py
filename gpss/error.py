# Base error class for all gpss.py errors
class Error(Exception):
	def __init__(self, filename, linenum, message):
		self.filename = filename
		self.linenum = linenum
		self.message = message

	def __str__(self):
		if self.filename is not None:
			filename = self.filename
		else:
			filename = "<instr>"
		if self.linenum is None:
			return f"{filename}: {self.message}"
		else:
			return f"{filename}({self.linenum}): {self.message}"

# Errors that occur during simulation
class SimulationError(Error):
	pass

# Violations of the gpss.py language
class ParserError(Error):
	pass

# Things that might be a mistake but also might not be
class ExecutionWarning:
	def __init__(self, filename, linenum, message):
		self.filename = filename
		self.linenum = linenum
		self.message = message

	def __str__(self):
		if self.filename is not None:
			filename = self.filename
		else:
			filename = "<instr>"
		if self.linenum is None:
			return f"{filename}: {self.message}"
		else:
			return f"{filename}({self.linenum}): {self.message}"
