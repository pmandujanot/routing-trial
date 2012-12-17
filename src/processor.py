#Import modules
import os
import csv
import model
import re


#Process files
def process_files(directory, data_id):
	#Get the filenames for the current proyect id
	busStopsFilePath = os.path.join(directory, str(data_id) + "-P.csv")
	schoolsFilePath = os.path.join(directory, str(data_id) + "-E.csv")
	routesFilePath = os.path.join(directory, str(data_id) + "-R.csv")

	#Parse files
	busStopsList = None
	schoolList = None
	routesList = None

	if os.path.isfile(busStopsFilePath):
		busStopsList = process_bus_stops(busStopsFilePath)

	if os.path.isfile(schoolsFilePath):
		schoolList = process_schools(schoolsFilePath)

	if os.path.isfile(routesFilePath):
		routesList = process_routes(routesFilePath)

	#Check if the files are OK
	if (busStopsList is not None) and (schoolList is not None) and (routesList is not None):

		#Process the data:
		process_data(busStopsList, schoolList, routesList)

		#Check if everything is OK

		return busStopsList, schoolList, routesList #{"busStops": busStopsList, "schools": schoolList, "routes": routesList}
	else:
		raise Exception("Error: No estan presentes los tres archivos con id: " + str(data_id))


#Process bus stops
def process_bus_stops(busStopsFilePath):
		
	#Create the busstop list
	busStopsList = []

	#Open the file and add it to the list
	with open(busStopsFilePath, 'r') as csvfile:
		busStopsReader = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
		for row in busStopsReader:
			#if len(row) == 0:
			#	continue
			
			#Check each of the busstop's parameters and create the busstop
			busStop = None
			try:
				#Get the ID
				bs_id = int(row["ID"])
				
				#Get the name
				nameMatch = re.match(r"''([\w\-]+)''", row["NAME"])
				name = nameMatch.group(1)

				#Get the location
				locationMatch = re.match(r"''(?P<latitude>[+-]?\d+(\.\d*)?);(?P<longitude>[+-]?\d+(\.\d*)?)''", row["LOCATION"])
				latitude = float(locationMatch.group('latitude'))
				longitude = float(locationMatch.group('longitude'))

				#Add the rest of the classes
				studentsOnClass = [int(row["#C1"]), int(row["#C2"]), int(row["#C3"]), int(row["#C4"])]

				#Create the object
				busStop = model.BusStop(bs_id, latitude, longitude, name, studentsOnClass)

			except Exception as e:
				raiseException = False
				for string in row.values():
					if string is not "":
						raiseException = True

				if raiseException:
					raise Exception("Error: Error parseando la parada de bus: " + str(row))

			#print busStop

			#Add the busttop to the 
			if busStop is not None:
				busStopsList.append(busStop)


		#print busStopsList;

		return busStopsList

def process_schools(schoolsFilePath):
		
	#Create the busstop list
	schoolList = []

	#Open the file and add it to the list
	with open(schoolsFilePath, 'r') as csvfile:
		schoolsReader = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
		for row in schoolsReader:
			#if len(row) == 0:
			#	continue
			
			#Check each of the school's parameters and create the busstop
			school = None
			try:
				#Get the ID
				s_id = int(row["ID"])
				
				#Get the name
				name = row["NAME"]

				#Get the location
				locationMatch = re.match(r"''(?P<latitude>[+-]?\d+(\.\d*)?);(?P<longitude>[+-]?\d+(\.\d*)?)''", row["LOCATION"])
				latitude = float(locationMatch.group('latitude'))
				longitude = float(locationMatch.group('longitude'))

				#Add the rest of the classes
				classCapacity = [int(row["#C1"]), int(row["#C2"]), int(row["#C3"]), int(row["#C4"])]

				#Create the object
				school = model.School(s_id, latitude, longitude, name, classCapacity)
				
			except Exception as e:
				raiseException = False
				for string in row.values():
					if string is not "":
						raiseException = True

				if raiseException:
					raise Exception("Error: Error parseando la escuela: " + str(row))

			#print school

			#Add the school to the 
			if school is not None:
				schoolList.append(school)


		#print schoolList;

		return schoolList

def process_routes(routessFilePath):
		
	#Create the busstop list
	routesList = []

	#Open the file and add it to the list
	with open(routessFilePath, 'r') as csvfile:
		routesReader = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
		for row in routesReader:
			#if len(row) == 0:
			#	continue
			
			#Check each of the route's parameters and create the busstop
			route = None
			try:
				#Get the ROUTE ID
				r_id = int(row["ROUTE"])

				#Get the BUSSTOP ID
				bs_id = int(row["ID"])

				#Get the SCHOOL ID
				s_id = int(row["ALLOC"])

				#Get the ORDER
				order = int(row["ORDER"])

				#Create the object
				route = model.Route(r_id, bs_id, s_id, order)
				
			except Exception as e:
				raiseException = False
				for string in row.values():
					if string is not "":
						raiseException = True

				if raiseException:
					raise Exception("Error: Error parseando la parada de ruta: " + str(row))

			#print route

			#Add the route to the 
			if route is not None:
				routesList.append(route)


		#print routesList;

		return routesList



def process_data(busStopsList, schoolList, routesList):
	#Process routes list and check if each route's busstop exists:
	for route in routesList:
		busStops = filter(lambda busStop: busStop.bs_id == route.bs_id, busStopsList)

		if len(busStops) == 1:
			route.busStop = busStops[0]
		else:
			raise Exception("Error: The route " + str(route.r_id) + "is related to an incorrect number of bus stops.")

	#Process all the schools and add the routes
	for school in schoolList:
		#Get all the routes for this school
		routes = filter(lambda route: route.s_id == school.s_id, routesList)

		#Split routes using route id
		routesDict = {}
		for route in routes:
			if route.r_id not in routesDict.keys():
				routesDict[route.r_id] = [route]
			else:
				routesDict[route.r_id].append(route)


		#print routesDict

		#Sort all routes using the value of the order parameter
		for routeList in  routesDict.values():	
			routeList.sort(key = lambda route: route.order)

		#TODO: check that the route order numbers are concecutive, if they are not, maybe a route number is missing.

		#Add the routes to the school
		school.routes = routesDict

		#print routes









#ahora que estoy abriendo el archivo y viendo las filas, tengo que ver dos cosas:
#parsear que los elementos en cada ppsicion esten bien (con regex supongo, por ejemplo para las coordenadas gps (las comillas y el ;))
#ver que el numero de elementos sea el correcto.
#con respeco a oop, cada una de las entradas de esta tabla puede ser un objeto de una clase que represente un paradero. Quiza el mismo objeto puede saber como parsearse a si mismo de la lista y crearse correctamente.
#en vez de imprimr en stdr y apagar el programa podria lanzar una excepcion la cual detector analizara y podra botar el programa si corresponde.








