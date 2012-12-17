#Import the necessary modules:
import sys #Command line arguments
import util 
import processor
import validator


#Get the proyect id
PROYECT_ID = None
if "--id" in sys.argv:
	idIndex = sys.argv.index("--id") + 1
	
	if idIndex < len(sys.argv):
		PROYECT_ID = util.convert_int(sys.argv[idIndex])

if PROYECT_ID is None:
	print "\nPlease specify the proyect_id using: --id\n"
	exit(1)

#Get the envvars
DATABASE_SERVER = util.get_from_env("DATABASE_SERVER", "192.168.1.100")
DATABASE_USERNAME = util.get_from_env("DATABASE_USERNAME", "routing")
DATABASE_PASSWORD = util.get_from_env("DATABASE_PASSWORD", "routing")
DATABASE_TYPE = util.get_from_env("DATABASE_TYPE", "Mysql")
DETECTOR_ROOT = util.get_path_from_env("DETECTOR_ROOT", "../data")


#Process the files for the current proyect_id
busStopsList, schoolList, routesList = processor.process_files(DETECTOR_ROOT, PROYECT_ID)

#Validate the data:
validator.validate_data(busStopsList, schoolList, routesList)

print "Archivos OK."



