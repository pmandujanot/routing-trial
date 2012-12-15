from SchoolModel import SchoolModel
from BusStopModel import BusStopModel
from RouteModel import RouteModel

class Model:
	"""Represents a optimization model"""

	def __init__(self, e, p, r):
		self.schools = {}
		self.bus_stops = {}
		self.routes = {}
		for school in e:
			self.schools[school.school_id] = school
		for bus_stop in p:
			self.bus_stops[bus_stop.bus_stop_id] = bus_stop
		for route in r:
			self.routes[route.route_id] = route
