
class BusStop:

	def __init__(self, bs_id, latitude, longitude, name, studentsOnClass):
		self.bs_id = bs_id
		self.longitude = longitude
		self.latitude = latitude
		self.name = name
		self.studentsOnClass = studentsOnClass

	def __repr__(self):
		description = str(self.bs_id) + " " + str(self.latitude) + " " + str(self.longitude) + " " + self.name
		for i in self.studentsOnClass:
			description += " " + str(i)

		return description

class School:

	def __init__(self, s_id, latitude, longitude, name, classCapacity):
		self.s_id = s_id
		self.longitude = longitude
		self.latitude = latitude
		self.name = name
		self.classCapacity = classCapacity
		self.routes = None

	def __repr__(self):
		description = str(self.s_id) + " " + str(self.latitude) + " " + str(self.longitude) + " " + self.name
		for i in self.classCapacity:
			description += " " + str(i)
		description += "\n" + str(self.routes) + "\n"

		return description

class Route:

	def __init__(self, r_id, bs_id, s_id, order):
		self.r_id = r_id
		self.bs_id = bs_id
		self.s_id = s_id
		self.order = order
		self.busStop = None

	def __repr__(self):
		description = str(self.r_id) + " " + str(self.bs_id) + " " + str(self.s_id) + " " + str(self.order)
		description += "\n" + str(self.busStop) + "\n"
		return description