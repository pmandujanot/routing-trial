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

			print busStop

			#Add the busttop to the 
			if busStop != None:
				busStopsList.append(busStop)


		#print busStopsList;

		return busStopsList














			





