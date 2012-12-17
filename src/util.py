#Import modules
import os 
import sys
import re


#Get the environment variable or return the default value
def get_from_env(var, default):
    if os.environ.has_key(var):
        return os.environ[var]
    else:
        return default

#Get the envvar and make sure it's a path
def get_path_from_env(var, default):
    path = get_from_env(var, default)
    if path and os.path.isdir(path):
        return path
    else:
        #Print the error and exit the program
        sys.stderr.write("\nERROR:\nEnvvar: " + var + "\nDefault: " + default + "\nPath: " + path + "\nPath is not a filename\n")
        exit(1)

#Parse int
def convert_int(intNum):
	try:
		return int(intNum)
	except ValueError:
		sys.stderr.write("Could not parse int\n")
		exit(1)


def get_all_proyect_ids_on_folder(folderPath):
    #Get all filenames on folder:
    fileNames = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath,f))]
    
    proyectIDs = set()
    for fileName in fileNames:
        try:
            nameMatch = re.match(r"(\d+)\-[EPR]\.csv", fileName)
            proyectID = int(nameMatch.group(1))
            proyectIDs.add(proyectID)
        except:
            pass

    return proyectIDs

