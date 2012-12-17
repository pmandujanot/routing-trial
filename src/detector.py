#Import the necessary modules:
import sys #Command line arguments
import util 
import processor
import validator
import dbmanager
import merger

#Get the proyect id
DATA_ID = None
if "--id" in sys.argv:
	idIndex = sys.argv.index("--id") + 1
	
	if idIndex < len(sys.argv):
		DATA_ID = util.convert_int(sys.argv[idIndex])

'''
if DATA_ID is None:
	print "\nPlease specify the DATA_id using: --id\n"
	exit(1)
'''

#Get the envvars
DATABASE_SERVER = util.get_from_env("DATABASE_SERVER", "192.168.1.102")
DATABASE_USERNAME = util.get_from_env("DATABASE_USERNAME", "routing")
DATABASE_PASSWORD = util.get_from_env("DATABASE_PASSWORD", "routing")
DATABASE_TYPE = util.get_from_env("DATABASE_TYPE", "Mysql")
DETECTOR_ROOT = util.get_path_from_env("DETECTOR_ROOT", "../data")

#Get the proyect ids
dataIDs = None
if DATA_ID is None:
	dataIDs = util.get_all_data_ids_on_folder(DETECTOR_ROOT)
else:
	dataIDs = set([DATA_ID])

#Instance database manager
dbManager = dbmanager.DatabaseManager(DATABASE_SERVER, DATABASE_USERNAME, DATABASE_PASSWORD)
dbManager.get_new_bucket_number()

#For each data-id, process data, validate it and merg it to the database.
for dataID in dataIDs:

	try:
		#Process the files for the current proyect_id
		print "\nLoading Data: " + str(dataID)
		busStopsList, schoolList, routesList = processor.process_files(DETECTOR_ROOT, dataID)

		#Validate the data:
		validator.validate_data(busStopsList, schoolList, routesList)
		print "All tests passed."

		#Get data from database
		dbSchoolsList = dbManager.load_data_from_database()

		#Merge data
		merger.merge_data(dbSchoolsList, schoolList, dbManager)


		#print schoolList
		#Save back to the database the modified data
		#dbManager.store_data(schoolList)


	except Exception as e:
		print e
		print "Purging ...OK"

	

#La idea podria ser que yo cargo de la base de datos, luego todas las cosas que cambiaron, como los tengo en objeto, podrias tener un bit dirty. luego con
#eso se si las tengo que guardar a la base de datos o no. Esto es porque si el nuevo archivo que estoy cargando sobreescribe el nombre de un colegio o algo asi
#al finla asumire que lo que manda son los parametros del rpimary key. 
#Otra cosa importante es que cuando haga el merge es necesario agregar las nuevos datos que van apareciendo, por ejemplo una nueva ruta.
#y si el numero de la ruta ya existe entonces se agrega reemplaza por la nueva ruta. Ahi hayq ue ver bien que se hace..

