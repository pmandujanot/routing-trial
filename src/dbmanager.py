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


	def store_data(self, schoolsList):
		db = self.get_db_instance()
		

		for school in schoolsList:
			cursor = db.cursor()
			try:
				#Store the school
				schoolSQL = "insert into Escuela(school_id, lat, lng, name, c_1, c_2, c_3, c_4, bucket) values (%i, %f, %f, '%s', %i, %i, %i, %i, '%s' ) \
								on duplicate key update lat = VALUES(lat), lng=VALUES(lng), name=VALUES(name), c_1 = VALUES(c_1), c_2=VALUES(c_2), c_3=VALUES(c_3), c_4=VALUES(c_4)" % \
						(school.s_id, school.latitude, school.longitude, school.name, school.classCapacity[0], school.classCapacity[1], school.classCapacity[2], school.classCapacity[3], "SCHOOL_LOAD_" + str(self.bucketNumber))

				cursor.execute(schoolSQL)

				for route in school.routes.values():
					for routeDetails in route:
						
						#Store BusStop
						busStop = routeDetails.busStop

						busstopSQL = "insert into Paradero(stop_id, lat, lng, name, p_1, p_2, p_3, p_4, bucket) values (%i, %f, %f, '%s', %i, %i, %i, %i, '%s' ) \
										on duplicate key update lat = VALUES(lat), lng=VALUES(lng), name=VALUES(name), p_1 = VALUES(p_1), p_2=VALUES(p_2), p_3=VALUES(p_3), p_4=VALUES(p_4)" % \
							(busStop.bs_id, busStop.latitude, busStop.longitude, busStop.name, busStop.studentsOnClass[0], busStop.studentsOnClass[1], busStop.studentsOnClass[2], busStop.studentsOnClass[3], "BUSSTOP_LOAD_"+str(self.bucketNumber))
						
						cursor.execute(busstopSQL)


						#Store the route element
						routeSQL = "insert into Ruta(stop_id, route_id, school_id, `order`, bucket) values (%i, %i, %i, %i, '%s') \
										on duplicate key update `order` = VALUES(`order`)" % \
							(routeDetails.bs_id, routeDetails.r_id, routeDetails.s_id, routeDetails.order, "ROUTES_LOAD_"+str(self.bucketNumber))
						
						cursor.execute(routeSQL)

				db.commit()

			except Exception as e:
				db.rollback()
				raise Exception(str(e))

		db.close()


	def get_new_bucket_number(self):
		db = self.get_db_instance()
		cursor = db.cursor()

		bucketNumber = 0

		cursor.execute("select distinct bucket from Paradero")
		buckets = cursor.fetchall()
		for bucket in buckets:
			bucketMatch = re.match(r"[\w\-_]+(\d+)", bucket[0])
			currentBucketNumber = int(bucketMatch.group(1))

			if bucketNumber < currentBucketNumber:
				bucketNumber = currentBucketNumber

		cursor.execute("select distinct bucket from Escuela")
		buckets = cursor.fetchall()
		for bucket in buckets:
			bucketMatch = re.match(r"[\w\-_]+(\d+)", bucket[0])
			currentBucketNumber = int(bucketMatch.group(1))

			if bucketNumber < currentBucketNumber:
				bucketNumber = currentBucketNumber

		cursor.execute("select distinct bucket from Paradero")
		buckets = cursor.fetchall()
		for bucket in buckets:
			bucketMatch = re.match(r"[\w\-_]+(\d+)", bucket[0])
			currentBucketNumber = int(bucketMatch.group(1))

			if bucketNumber < currentBucketNumber:
				bucketNumber = currentBucketNumber

		bucketNumber += 1

		self.bucketNumber = bucketNumber
		db.close()

		return bucketNumber











