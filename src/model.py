
class BusStop:

	def __init__(self, bs_id, longitude, latitude, name, classes):
		self.bs_id = bs_id
		self.longitude = longitude
		self.latitude = latitude
		self.name = name
		self.classes = classes

	def __repr__(self):
		description = str(self.bs_id) + " " + str(self.longitude) + " " + str(self.latitude) + " " + self.name
		for i in self.classes:
			description += " " + str(i)

		return description

