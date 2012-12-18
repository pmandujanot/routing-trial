"""Detector.py MVP for RoutingUC Test

Author: Jose Tomas Robles Hahn
"""

import sys
import csv
import string
import MySQLdb
import os
from haversine import distance


class Detector():
	def __init__(self, dbconfig, problemId,tempDBname="myTempDB",debug=False):
		self.dbconfig = dbconfig
		self.problemId = problemId
		self.tempDBname = tempDBname
		self.errorCount = 0
		self.debug = debug

	
	def reportValidationError(self, msg):
		"Prints validation error message and increments error counter."
		
		print "Validation ERROR: " + msg
		self.errorCount += 1
		
	
	def reportWarning(self, msg):
		"Prints warning message. Warnings are for informational use only and are not considered errors."
		print "WARNING: " + msg
		
	
	def printDebug(self, msg):
		"Prints debug messages if debugging is enabled (self.debug is true)."
		if self.debug == True:
			print "DEBUG: " + msg
	
	
	def importIntoTempDB(self):
		"Import CSV files into temporary database"
		
		def reportEmptyValueWarning(csvFilename, row):
			self.reportWarning("CSV record in %s contains at least one field with at least one empty value: %s" % (csvFilename, str(row)))
			
		def importParaderosIntoTempDB():
			"Import paraderos CSV file into temporary database"
		
			cursor.execute("""CREATE TABLE Paradero (
				STOP_ID INTEGER,
				LAT FLOAT,
				LNG FLOAT,
				NAME VARCHAR(255),
				P_1 INTEGER,
				P_2 INTEGER,
				P_3 INTEGER,
				P_4 INTEGER,
				BUCKET VARCHAR(255)
				)""")
			
			csvFilename = self.problemId + "-P.csv"
			with open(csvFilename, 'rt') as csvFile:
				csvRows = csv.reader(csvFile)
				csvRows.next() # Skip header line
			
				for row in csvRows:
					if row[0] and row[1] and row[2] and row[3] and row[4] and row[5] and row[6]: # row must have a value in each field
						location = string.split(string.strip(row[1], "''"),';')
						parsedRow = [row[0], # STOP_ID
							location[0], location[1], # LAT, LNG
							string.strip(row[2], "''"), # NAME
							row[3], row[4], row[5], row[6], # P_1, P_2, P_3, P_4
							'ROUTE_LOAD_' + self.problemId] # BUCKET
						cursor.execute('INSERT INTO Paradero VALUES (%s, %s, %s, "%s", %s, %s, %s, %s, "%s")', parsedRow)
					else:
						reportEmptyValueWarning(csvFilename, row)
		
		
		def importEscuelasIntoTempDB():
			"Import escuelas CSV file into temporary database"
			
			cursor.execute("""CREATE TABLE Escuela (
				SCHOOL_ID INTEGER,
				LAT FLOAT,
				LNG FLOAT,
				NAME VARCHAR(255),
				C_1 INTEGER,
				C_2 INTEGER,
				C_3 INTEGER,
				C_4 INTEGER,
				BUCKET VARCHAR(255)
				)""")

			csvFilename = self.problemId + "-E.csv"
			with open(csvFilename, 'rt') as csvFile:
				csvRows = csv.reader(csvFile)
				csvRows.next() # Skip header line
			
				for row in csvRows:
					if row[0] and row[1] and row[2] and row[3] and row[4] and row[5] and row[6]: # row must have a value in each field
						location = string.split(string.strip(row[1], "''"),';')
						parsedRow = [row[0], # SCHOOL_ID
							location[0], location[1], # LAT, LNG
							string.strip(row[2], "''"), # NAME
							row[3], row[4], row[5], row[6], # C_1, C_2, C_3, C_4
							'ROUTE_LOAD_' + self.problemId] # BUCKET
						cursor.execute('INSERT INTO Escuela VALUES (%s, %s, %s, "%s", %s, %s, %s, %s, "%s")', parsedRow)
					else:
						reportEmptyValueWarning(csvFilename, row)
		
		def importRutasIntoTempDB():
			"Import rutas CSV file into temporary database"
			
			cursor.execute("""CREATE TABLE Ruta (
				STOP_ID INTEGER,
				ROUTE_ID INTEGER,
				SCHOOL_ID INTEGER,
				`ORDER` INTEGER,
				BUCKET VARCHAR(255)
				)""")
		
			csvFilename = self.problemId + "-R.csv"
			with open(csvFilename, 'rt') as csvFile:
				csvRows = csv.reader(csvFile)
				csvRows.next() # Skip header line
			
				for row in csvRows:
					if row[0] and row[1] and row[2] and row[3]: # row must have a value in each field
						parsedRow = [row[0], # STOP_ID
							row[1], # ROUTE_ID
							row[2], # SCHOOL_ID
							row[3], # ORDER
							'ROUTE_LOAD_' + self.problemId] # BUCKET
						cursor.execute('INSERT INTO Ruta VALUES (%s, %s, %s, %s, %s)', parsedRow)
					else:
						reportEmptyValueWarning(csvFilename, row)
			
		
		dbconn = MySQLdb.connect(self.dbconfig["server"], user=self.dbconfig["username"], passwd=self.dbconfig["password"])
		cursor = dbconn.cursor()
		cursor.execute('CREATE DATABASE ' + self.tempDBname)
		cursor.execute('USE ' + self.tempDBname)
		
		importParaderosIntoTempDB()
		importEscuelasIntoTempDB()
		importRutasIntoTempDB()
			
		dbconn.commit()
		cursor.close()
		dbconn.close()
		

	def validateDuplicateKeys(self, cursor):
		"Verifies some fields that should be unique so that they do not mess with the other validation tests."
		# CSV files supplied with the test violated some of the following tests.
		# For example, one 1-E.csv has three records with ID=148 that make validateSchoolClassCapacity return invalid results.

		sql = "SELECT STOP_ID, count(*) FROM Paradero GROUP BY STOP_ID HAVING count(*) > 1;"
		cursor.execute(sql)
		
		if cursor.rowcount > 0:
			self.reportValidationError("Multiple bus stops with same STOP_ID in Paradero. First duplicate: STOP_ID=%s" % cursor.fetchone()[0])
		else:
			self.printDebug("OK: No duplicate STOP_IDs in Paradero")

		
		sql = "SELECT SCHOOL_ID, count(*) FROM Escuela GROUP BY school_id HAVING count(*) > 1;"
		cursor.execute(sql)
		
		if cursor.rowcount > 0:
			self.reportValidationError("Schools with duplicate School_IDs in Escuela. First duplicate: SCHOOL_ID=%s" % cursor.fetchone()[0])
		else:
			self.printDebug("OK: No duplicate SCHOOL_IDs in Escuela")

		
		sql = "SELECT STOP_ID, count(*) FROM Ruta GROUP BY STOP_ID HAVING count(*) > 1;"
		cursor.execute(sql)
		
		if cursor.rowcount > 0:
			self.reportValidationError("STOP_ID with more than one route including it in Ruta. First STOP_ID=%s" % cursor.fetchone()[0])
		else:
			self.printDebug("OK: No duplicate STOP_IDs in Ruta")

	
	def validateSchoolClassCapacity(self, cursor):
		"Validate school class capacity"
		
		sql = """SELECT E.SCHOOL_ID, E.NAME as SCHOOL_NAME, E.C_1, E.C_2, E.C_3, E.C_4, sum(P.P_1) as Sum_P_1, sum(P.P_2) as Sum_P_2, sum(P.P_3) as Sum_P_3, sum(P.P_4) as Sum_P_4
FROM Escuela E, Paradero P, Ruta R
WHERE E.SCHOOL_ID = R.SCHOOL_ID and P.STOP_ID = R.STOP_ID
GROUP BY E.SCHOOL_ID
HAVING Sum_P_1 > C_1 or Sum_P_2 > C_2 or Sum_P_3 > C_3 or Sum_P_4 > C_4
ORDER BY E.SCHOOL_ID;"""
		cursor.execute(sql)
		
		if cursor.rowcount > 0:
			firstRecord = cursor.fetchone()
			self.reportValidationError("School class capacity exceeded in %s school(s). First school: School_ID=%s (%s) Capacity/Students for C1:%s/%s C2:%s/%s C3:%s/%s C4:%s/%s" % \
			(cursor.rowcount, firstRecord[0], firstRecord[1], \
			firstRecord[2], firstRecord[6], \
			firstRecord[3], firstRecord[7], \
			firstRecord[4], firstRecord[8], \
			firstRecord[5], firstRecord[9]) \
			)
		else:
			self.printDebug("OK: No school class capacities exceeded")

		
	def validateRouteForEveryStop(self, cursor):
		"Verify that every bus stop is included in a route."

		sql = """SELECT P.STOP_ID AS P_STOPID, P.NAME, R.STOP_ID AS R_STOPID, R.SCHOOL_ID
FROM Paradero P
LEFT OUTER JOIN Ruta R on P.STOP_ID = R.STOP_ID
WHERE R.STOP_ID is NULL;"""
		cursor.execute(sql)
		
		if cursor.rowcount > 0:
			firstRecord = cursor.fetchone()
			self.reportValidationError("%s bus stop(s) without route(s) including it/them. First bus stop ID=%s (%s)" % (cursor.rowcount, firstRecord[0], firstRecord[1]))
		else:
			self.printDebug("OK: No bus stops without a route including it.")

		
	def validateMaxRouteLength(self, cursor1, cursor2):
		"Verify that no route exceeds the maximum allowed length"
		
		maxRouteLength = 35 # km
		
		sql = "SELECT DISTINCT R.ROUTE_ID FROM Ruta R ORDER BY R.ROUTE_ID"
		cursor1.execute(sql)
		
		def calculateRouteLength(routeId):
			"Returns the length of the route identified by routeId"
			
			totalRouteLength = 0
			
			sql = """(SELECT P.LAT, P.LNG FROM Paradero P, Ruta R WHERE R.ROUTE_ID = %s and P.STOP_ID = R.STOP_ID ORDER BY R.ORDER)
UNION (SELECT E.LAT, E.LNG FROM Escuela E, Ruta R WHERE R.ROUTE_ID = %s and R.SCHOOL_ID = E.SCHOOL_ID);"""
			cursor2.execute(sql, (routeId[0], routeId[0]))
			
			if cursor2.rowcount > 1:
				origin = cursor2.fetchone()
				for i in range(cursor2.rowcount - 1):
					destination = cursor2.fetchone()
					totalRouteLength = totalRouteLength + distance(origin, destination)
					origin = destination
			
			return totalRouteLength
			
		self.printDebug("Calculating distance for %s routes" % cursor1.rowcount)
		
		for i in range(cursor1.rowcount):
			routeId = cursor1.fetchone()
			routeLength = calculateRouteLength(routeId)
			
			if routeLength > maxRouteLength:
				self.reportValidationError("Route with ID=%s exceeds maximum route length of %s km: %s km" % (routeId[0], maxRouteLength, routeLength))


	def validateBusCapacity(self, cursor):
		"Verify that no bus ends up transporting more than the allowed number of passengers"

		busCapacity = 45 # passengers
		sql = """SELECT R.ROUTE_ID, SUM(P.P_1) as SUM_P_1, SUM(P.P_2) as SUM_P_2, SUM(P.P_3) as SUM_P_3, SUM(P.P_4) as SUM_P_4, SUM(P.P_1)+SUM(P.P_2)+SUM(P.P_3)+SUM(P.P_4) as SUM_P_TOTAL
FROM Paradero P, Ruta R
WHERE R.STOP_ID = P.STOP_ID
GROUP BY R.ROUTE_ID
HAVING SUM_P_TOTAL > %s;"""
		cursor.execute(sql, busCapacity)
		
		if cursor.rowcount > 0:
			firstRecord = cursor.fetchone()
			self.reportValidationError("%s bus route(s) exceeding bus capacity of %s passengers. First route: ROUTE_ID=%s Passengers=%s" % \
			(cursor.rowcount, busCapacity, firstRecord[0], firstRecord[5]))
		else:
			self.printDebug("OK: No bus routes exceeding bus capacity of %s passengers" % busCapacity)


	def runValidations(self):
		"Run validation test set"
		
		dbconn = MySQLdb.connect(self.dbconfig["server"], user=self.dbconfig["username"], passwd=self.dbconfig["password"], db=self.tempDBname)
		cursor = dbconn.cursor()
		cursor2 = dbconn.cursor()
		
		self.validateDuplicateKeys(cursor)
		self.validateSchoolClassCapacity(cursor)
		self.validateRouteForEveryStop(cursor)
		self.validateMaxRouteLength(cursor, cursor2)
		self.validateBusCapacity(cursor)
		
		cursor.execute('DROP DATABASE ' + self.tempDBname) # Delete temporary database after validations have finished
		dbconn.commit()
		cursor.close()
		cursor2.close()
		dbconn.close()
		
	
	def start(self):
		"Import CSV files into temporary database and run validation tests"

		self.importIntoTempDB()
		self.runValidations()


if __name__ == "__main__":
	dbconfig = {"server": os.environ['DATABASE_SERVER'],
					"username": os.environ['DATABASE_USERNAME'],
					"password": os.environ['DATABASE_PASSWORD']}

	if len(sys.argv) == 3 and sys.argv[1] == "--id" and sys.argv[2]:
		if os.path.isfile(sys.argv[2]+"-P.csv") \
			and os.path.isfile(sys.argv[2]+"-E.csv") \
			and os.path.isfile(sys.argv[2]+"-R.csv"):
			
			print "**** Creating Detector for Problem %s ..." % sys.argv[2]
			d = Detector(dbconfig, sys.argv[2])
			print "**** Starting Detector..."
			d.start()
			
			if d.errorCount == 0:
				print "**** SUCCESS: CSV files have passed validation ****"
			else:
				print "**** FAILURE: CSV files have %s validation error(s) ****" % d.errorCount
			
		else:
			print "ERROR: Verify that files %s-P.csv, %s-E.csv, %s-R.csv exist" % (sys.argv[2], sys.argv[2], sys.argv[2])
	else:
		print """Usage: %s --id <Problem_ID>
Example: %s --id 2""" % (sys.argv[0], sys.argv[0])