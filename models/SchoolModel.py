import re

class SchoolModel:
	"""Represents a school"""

	def __init__(self):
		self.school_id = 0
		self.location = [0,0]
		self.name = ""
		self.c = {}


	def load_from_csv(self, row):
		self.school_id = row[0]
		# parse location from string
		match = re.search(r"''(-?\d+\.\d+);(-?\d+\.\d+)''", row[1])
		self.location = [float(match.group(1)), float(match.group(2))]
		self.name = row[2].strip("'")
		for i in range(3,7):
			self.c[i-3] = int(row[i])
