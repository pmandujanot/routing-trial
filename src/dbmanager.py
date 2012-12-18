import MySQLdb
import model
import re

class DatabaseManager:

	def __init__(self, serverAddress, username, password):
		self.serverAddress = serverAddress
		self.username = username
		self.password = password
		self.bucketNumber = 0


	def get_db_instance(self):
		return MySQLdb.connect(host = self.serverAddress, user = self.username, passwd = self.password, db = self.username)


	def get_new_bucket_number(self):
		db = self.get_db_instance()
		cursor = db.cursor()

		bucketNumber = -1

		for tableName in ["Paradero", "Escuela", "Ruta"]:
			cursor.execute("select distinct BUCKET from " + tableName)
			buckets = cursor.fetchall()
			for bucket in buckets:
				bucketMatch = re.match(r"[\w\-_]+(\d+)", bucket[0])
				currentBucketNumber = int(bucketMatch.group(1))

				if bucketNumber < currentBucketNumber:
					bucketNumber = currentBucketNumber

		bucketNumber += 1
		db.close()

		self.bucketNumber = bucketNumber
		return bucketNumber

	def init_database(self):
		db = self.get_db_instance()
		cursor = db.cursor()

		try:
			cursor.execute('''create table if not exists Escuela (
				SCHOOL_ID integer,
				LAT float,
				LNG float,
				NAME varchar(255),
				C_1 integer,
				C_2 integer,
				C_3 integer,
				C_4 integer,
				BUCKET varchar(255),
				constraint primary key(SCHOOL_ID, BUCKET)
				);''')

			cursor.execute('''create table if not exists Paradero (
				STOP_ID integer,
				LAT float,
				LNG float,
				NAME varchar(255),
				P_1 integer,
				P_2 integer,
				P_3 integer,
				P_4 integer,
				BUCKET varchar(255),
				constraint primary key(STOP_ID, BUCKET)
				);''')

			cursor.execute('''create table if not exists Ruta (
				STOP_ID integer,
				ROUTE_ID integer,
				SCHOOL_ID integer,
				`ORDER` integer,
				BUCKET varchar(255),
				constraint primary key(STOP_ID, ROUTE_ID, SCHOOL_ID, BUCKET),
				constraint foreign key(STOP_ID) references Paradero(STOP_ID),
				constraint foreign key(SCHOOL_ID) references Escuela(SCHOOL_ID)
				);''')
			db.commit()
		
		except Exception as e:
			db.rollback()
			print "Error: Error creando la base de datos"
			print e
			db.close()
			exit(1)


		db.close()


	def configure(self):
		self.init_database()
		self.get_new_bucket_number()


	def store_data(self, schoolsList):
		db = self.get_db_instance()
		

		for school in schoolsList:
			cursor = db.cursor()
			try:
				#Store the school
				schoolSQL = "insert into Escuela(SCHOOL_ID, LAT, LNG, NAME, C_1, C_2, C_3, C_4, BUCKET) values (%i, %f, %f, '%s', %i, %i, %i, %i, '%s' ) \
								on duplicate key update LAT = VALUES(LAT), LNG=VALUES(LNG), NAME=VALUES(NAME), C_1 = VALUES(C_1), C_2=VALUES(C_2), C_3=VALUES(C_3), C_4=VALUES(C_4)" % \
						(school.s_id, school.latitude, school.longitude, school.name, school.classCapacity[0], school.classCapacity[1], school.classCapacity[2], school.classCapacity[3], "SCHOOL_LOAD_" + str(self.bucketNumber))

				cursor.execute(schoolSQL)

				for route in school.routes.values():
					for routeDetails in route:
						
						#Store BusStop
						busStop = routeDetails.busStop

						busstopSQL = "insert into Paradero(STOP_ID, LAT, LNG, NAME, P_1, P_2, P_3, P_4, BUCKET) values (%i, %f, %f, '%s', %i, %i, %i, %i, '%s' ) \
										on duplicate key update LAT = VALUES(LAT), LNG=VALUES(LNG), NAME=VALUES(NAME), P_1 = VALUES(P_1), P_2=VALUES(P_2), P_3=VALUES(P_3), P_4=VALUES(P_4)" % \
							(busStop.bs_id, busStop.latitude, busStop.longitude, busStop.name, busStop.studentsOnClass[0], busStop.studentsOnClass[1], busStop.studentsOnClass[2], busStop.studentsOnClass[3], "BUSSTOP_LOAD_"+str(self.bucketNumber))
						
						cursor.execute(busstopSQL)


						#Store the route element
						routeSQL = "insert into Ruta(STOP_ID, ROUTE_ID, SCHOOL_ID, `ORDER`, BUCKET) values (%i, %i, %i, %i, '%s') \
										on duplicate key update `ORDER` = VALUES(`ORDER`)" % \
							(routeDetails.bs_id, routeDetails.r_id, routeDetails.s_id, routeDetails.order, "ROUTES_LOAD_"+str(self.bucketNumber))
						
						cursor.execute(routeSQL)

				db.commit()

			except Exception as e:
				db.rollback()
				raise Exception(str(e))

		db.close()





	def load_data_from_database(self):
		db = self.get_db_instance()
		cursor = db.cursor()

		#Get the schools from the database
		schoolSQL = "select * from Escuela where BUCKET = '%s' " % ("SCHOOL_LOAD_" + str(self.bucketNumber))
		cursor.execute(schoolSQL)
		schoolRows = cursor.fetchall()

		schoolsList = []
		for row in schoolRows:
			#Get the class capacity list
			classCapacity = [row[4], row[5], row[6], row[7]]

			#Create the object
			school = model.School(row[0], row[1], row[2], row[3], classCapacity)

			#Add the object to the list
			schoolsList.append(school)


		#Get the Bus Stops from the database
		busstopSQL = "select * from Paradero where BUCKET = '%s' " % ("BUSSTOP_LOAD_" + str(self.bucketNumber))
		cursor.execute(busstopSQL)
		busStopRows = cursor.fetchall()

		busStopsList = []
		for row in busStopRows:
			#Get the the students of each class waiting for the bus
			studentsOnClass = [row[4], row[5], row[6], row[7]]

			#Create the object
			busStop = model.BusStop(row[0], row[1], row[2], row[3], studentsOnClass)

			#Add the object to the list
			busStopsList.append(busStop)


		#Get the Bus Stops from the database
		routesSQL = "select * from Ruta where BUCKET = '%s' " % ("ROUTES_LOAD_" + str(self.bucketNumber))
		cursor.execute(routesSQL)
		routesRows = cursor.fetchall()

		routesList = []
		for row in routesRows:
			#Create the object
			route = model.Route(row[1], row[0], row[2], row[3])

			#Add the object to the list
			routesList.append(route)


		#Process the data:
		from processor import process_data
		process_data(busStopsList, schoolsList, routesList)


		db.close()

		return schoolsList


	def delete_route(self, routeList):
		db = self.get_db_instance()
		cursor = db.cursor()

		for routeDetails in routeList:
			
			#Delete the related busstop
			busStop = routeDetails.busStop
			cursor.execute("delete from Paradero where STOP_ID = %i and BUCKET = '%s'" % (busStop.bs_id, "BUSSTOP_LOAD_" + str(self.bucketNumber)))

			#Delete the route details
			cursor.execute("delete from Ruta where ROUTE_ID = %i and STOP_ID = %i and SCHOOL_ID = %i and BUCKET = '%s'" % \
				(routeDetails.r_id, routeDetails.bs_id, routeDetails.s_id, "ROUTES_LOAD_" + str(self.bucketNumber)))			

		db.commit()
		db.close()



