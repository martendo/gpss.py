class Function:
	def __init__(self, type_, arg, points, name):
		self.simulation = None
		self.type = type_
		self.arg = arg
		self.points = points
		self.name = name

	def __str__(self):
		return f"Function \"{self.name}\": RN{self.arg}, {self.type}{len(self.points)}"

	def __call__(self):
		if self.simulation is None:
			raise TypeError("Function is not bound to a Simulation")

		if self.type == "D":
			val = self.simulation.rngs[self.arg].random()
			for point in self.points:
				if point[0] >= val:
					break
			return point[1]
		else:
			raise NotImplementedError("Only discrete Functions have yet to be implemented")
