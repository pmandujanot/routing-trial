
class SchoolModel:
	"""Represents a school"""

	def __init__(self):
		self.school_id = 0
		self.location = ""
		self.name = ""
		self.c = {}


	def load_from_csv(self, row):
		self.school_id = row[0]
		self.location = row[1]
		self.name = row[2]
		for i in range(3,7):
			self.c[i-3] = int(row[i])
