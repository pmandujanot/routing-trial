
class RouteModel:
	"""Represents a route"""

	def __init__(self):
		self.route_id = 0
		self.bus_stop_id = 0
		self.alloc_id = 0
		self.order = 0


	def load_from_csv(self, row):
		self.bus_stop_id = row[0]
		self.route_id = row[1]
		self.alloc_id = row[2]
		self.order = int(row[3])
