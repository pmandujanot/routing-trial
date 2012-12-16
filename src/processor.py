#Import modules
import os
import csv
import model
import re


#Process files
def process_files(directory, proyect_id):
	#Get the filenames for the current proyect id
	busStopsFilePath = os.path.join(directory, str(proyect_id) + "-P.csv")
	schoolsFilePath = os.path.join(directory, str(proyect_id) + "-E.csv")
	routesFilePath = os.path.join(directory, str(proyect_id) + "-R.csv")

	#Parse files
	if os.path.isfile(busStopsFilePath):
		process_bus_stops(busStopsFilePath)

	if os.path.isfile(schoolsFilePath):
		process_schools(schoolsFilePath)

	if os.path.isfile(routesFilePath):
		process_routes(routesFilePath)


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
				classes = [int(row["#C1"]), int(row["#C2"]), int(row["#C3"]), int(row["#C4"])]

				#Create the object
				busStop = model.BusStop(bs_id, latitude, longitude, name, classes)

			except Exception as e:
				print e

			#print busStop

			#Add the busttop to the 
			if busStop != None:
				busStopsList.append(busStop)


		print busStopsList;

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
			
			#Check each of the busstop's parameters and create the busstop
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
				print e

			#print school

			#Add the school to the 
			if school != None:
				schoolList.append(school)


		print schoolList;

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
			
			#Check each of the busstop's parameters and create the busstop
			route = None
			try:
				#Get the ID
				r_id = int(row["ROUTE"])

				#Get the ID
				bs_id = int(row["ID"])

				#Get the ID
				s_id = int(row["ALLOC"])

				#Get the ID
				order = int(row["ORDER"])

				#Create the object
				route = model.Route(r_id, bs_id, s_id, order)
				
			except Exception as e:
				print e

			#print route

			#Add the route to the 
			if route != None:
				routesList.append(route)


		print routesList;

		return routesList










			#ahora que estoy abriendo el archivo y viendo las filas, tengo que ver dos cosas:
			#parsear que los elementos en cada ppsicion esten bien (con regex supongo, por ejemplo para las coordenadas gps (las comillas y el ;))
			#ver que el numero de elementos sea el correcto.
			#con respeco a oop, cada una de las entradas de esta tabla puede ser un objeto de una clase que represente un paradero. Quiza el mismo objeto puede saber como parsearse a si mismo de la lista y crearse correctamente.
			#en vez de imprimr en stdr y apagar el programa podria lanzar una excepcion la cual detector analizara y podra botar el programa si corresponde.








