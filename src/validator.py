import model
import math


def validate_data(busStopsList, schoolList, routesList):

	#Validation 1: Amount of children must not be greater than the capacity of the school
	validate_amount_of_children_on_class(schoolList)

	#Validation 2: All busstops must be enrouted
	validate_bus_stops_on_routes(busStopsList, schoolList)

	#Validation 3: All routes must not be longer than 35 kms
	validate_route_length(schoolList)

	#Validation 4: Amount of children must not be greater than the capacity of the bus
	validate_amount_of_children_on_bus(schoolList)




def validate_amount_of_children_on_class(schoolList):
	#For each of the schools, check if the kids waiting for each class on all busstops are less or equal than the class capacity
	for school in schoolList:
		
		studentsWaitingForClass = [0,0,0,0]
		for routes in school.routes.values():
			for routeItem in routes:
				for i in range(0,4):
					studentsWaitingForClass[i] += routeItem.busStop.studentsOnClass[i]


		#print studentsWaitingForClass

		for i in range(0,4):
			if studentsWaitingForClass[i] > school.classCapacity[i]:
				raise Exception("Error: Cantidad de alumnos (" + str(studentsWaitingForClass[i]) + ") supera la capacidad de la clase #C" + str(i+1) + " de la escuela " + school.name + ".")



def validate_bus_stops_on_routes(busStopsList, schoolList):
	#Duplicate busstop list
	busStops = busStopsList[:]

	#On all schools 
	for school in schoolList:
		for routes in school.routes.values():
			for routeItem in routes:
				if routeItem.busStop in busStops:
					busStops.remove(routeItem.busStop)

	#Print the unrouted busstops
	if len(busStops) > 0:
		description = "Error: Los siguientes paraderos no estan enrutados: \n"
		for busStop in busStops:
			description += "\t-" + str(busStop.bs_id)

		raise Exception(description)


def validate_route_length(schoolList):
	#Las rutas parten en el item con order=1 y terminan en el colegio.

	#For each school we get the route and add it's lengths using the harvesine distance
	for school in schoolList:
		#We add the route 
		for routeID in school.routes.keys():
			previousBusStop = None
			routeDistance = 0.0
			
			for routeItem in school.routes[routeID]:
				if previousBusStop is not None:
					routeDistance += harvesine_distance([routeItem.busStop.latitude,routeItem.busStop.longitude],[previousBusStop.latitude,previousBusStop.longitude])
				previousBusStop = routeItem.busStop

			if previousBusStop is not None:
				routeDistance += harvesine_distance([school.latitude,school.longitude],[previousBusStop.latitude,previousBusStop.longitude])

			if routeDistance > 35000:
				raise Exception("Error: Ruta " + str(routeID) + " de la escuela " + school.name + " es mayor a 35KM (" + str(routeDistance/1000) + ")")


#Position a and b are in [latitude, longitude]
def harvesine_distance (a, b):
	rad_per_deg = math.pi/180  # PI / 180
	rkm = 6371                  # Earth radius in kilometers
	rm = rkm * 1000             # Radius in meters

	dlon_rad = (b[1]-a[1]) * rad_per_deg  # Delta, converted to rad
	dlat_rad = (b[0]-a[0]) * rad_per_deg

	lat1_rad, lon1_rad = map(lambda i: i*rad_per_deg, a)
	lat2_rad, lon2_rad = map(lambda i: i*rad_per_deg, b)

	a = math.sin(dlat_rad/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2
	c = 2 * math.asin(math.sqrt(a))

	return rm * c # Delta in meters


def validate_amount_of_children_on_bus(schoolList):
	#For each of the schools, check if the kids waiting for the bus on all busstops of that route are greater than the capacity of the bus
	for school in schoolList:
		for routeID in school.routes.keys():
			studentsWaitingForBus = 0
			for routeItem in school.routes[routeID]:
				for i in range(0,4):
					studentsWaitingForBus += routeItem.busStop.studentsOnClass[i]

			if studentsWaitingForBus > 45:
				raise Exception("Error: Cantidad de alumnos (" + str(studentsWaitingForBus) + ") supera la capacidad del bus (45) de la ruta " + str(routeID) + " de la escuela " + school.name + ".")
				


