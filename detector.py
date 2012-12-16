#!/usr/bin/python
import argparse
import csv
import math
import os
import sys
from models.SchoolModel import SchoolModel
from models.BusStopModel import BusStopModel
from models.RouteModel import RouteModel
from models.Model import Model


def load_envvars():
	"""Loads environment variables"""
	global DETECTOR_ROOT, DATABASE_SERVER, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_TYPE
	DETECTOR_ROOT = os.getenv('DETECTOR_ROOT', 'data')
	DATABASE_SERVER = os.getenv('DATABASE_SERVER', 'localhost')
	DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'routing')
	DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'routing')
	DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'mysql').lower()


def load_csv(filename, class_type):
	"""Loads a CSV file"""
	try:
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			objects = []
			reader.next()	# skip the header
			for row in reader:
				if row.count('') == len(row):
					continue	# skip empty rows
				# instantiate an object for each model entry
				obj = class_type()
				obj.load_from_csv(row)
				objects.append(obj)
			return objects
	except IOError as e:
		print(e)
		return None
	#except csv.Error as e:
	except Exception as e:
		print('error parsing file %s, line %d: %s' % (filename, reader.line_num, e))
		return None


def load_model(id):
	"""Loads a model from its CSV files"""
	print("LOADING data " + str(id))
	e = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-E.csv'), SchoolModel)
	p = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-P.csv'), BusStopModel)
	r = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-R.csv'), RouteModel)
	if (e is None) or (p is None) or (r is None):
		return None
	return Model(e, p, r)


def validate_model_school_capacity(model):
	""" Checks that the number of students for each school is not greater than its capacity"""
	errors = []
	# init student count at each school for each course at 0
	student_counts = {}
	for school in model.schools.values():
		student_counts[school.school_id] = {}
		for c in school.c.keys():
			student_counts[school.school_id][c] = 0
	# count students in stops
	for route in model.routes.values():
		for r in route:
			stop = model.bus_stops[r.bus_stop_id]
			for c in stop.c.items():
				student_counts[r.alloc_id][c[0]] += c[1]
	# validate
	for school in model.schools.values():
		for c in school.c.items():
			if student_counts[school.school_id][c[0]] > c[1]:
				errors.append("Error: School {0} ({4}) has {1} students for course {2} (max: {3})".format(
					school.school_id,
					student_counts[school.school_id][c[0]],
					c[0],
					c[1],
					school.name))
	return errors


def validate_model_bus_stops_in_route(model):
	"""All bus stops must belong to a route"""
	errors = []
	valid_stops = set()
	# count valid bus_stops
	for route in model.routes.values():
		for r in route:
			valid_stops.add(r.bus_stop_id)
	# validate
	for stop in model.bus_stops.values():
		if not valid_stops.issuperset([stop.bus_stop_id]):
			errors.append("Error: Bus stop {0} doesn't belong to any route.".format(stop.bus_stop_id))
	return errors


def validate_model_max_route_length(model):
	"""All routes are under 35km in length"""
	errors = []
	for route in model.routes.values():
		# calculate distance
		distance = 0
		i = 0
		if len(route) > 1:
			for i in range(1, len(route)):
				distance += dist_harvesine(model.bus_stops[route[i-1].bus_stop_id].location, 
											model.bus_stops[route[i].bus_stop_id].location)
		distance += dist_harvesine(model.bus_stops[route[i].bus_stop_id].location, 
									model.schools[route[i].alloc_id].location)
		# validate
		if distance > 35:
			errors.append("Error: Route {0} is {1} km long (max: 35 km)".format(route[0].route_id, distance))
	return errors


def validate_model_max_bus_capacity(model):
	"""Students in a route must not exceed 45 students"""
	errors = []
	for route in model.routes.values():
		# count students in route
		student_count = 0
		for r in route:
			student_count += sum(model.bus_stops[r.bus_stop_id].c.values())
		# validate
		if student_count > 45:
			errors.append("Error: Route {0} has {1} students in a bus (max: 45)".format(route[0].route_id, student_count))
	return errors


def dist_harvesine(origin_coords, destination_coords):
	"""Distance between 2 objects"""
	lat1, lon1 = origin_coords
	lat2, lon2 = destination_coords
	radius = 6371 # km

	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c
	return d


def validate_model(model):
	"""Perform all model validations"""
	validation_funcs = [validate_model_school_capacity,
						validate_model_bus_stops_in_route,
						validate_model_max_route_length,
						validate_model_max_bus_capacity]

	success = True
	for f in validation_funcs:
		errors = f(model)
		if errors:
			for e in errors:
				print(e)
			success = False

	if success:
		print("ALL TESTS PASSED")
	return success


def merge_model(model):
	"""Insert into DB"""
	print("MERGING...")
	# TODO
	print("OK")
	return True


def main(id):
	"""Load, validate, and merge model"""
	model = load_model(id)
	if model is not None:
		if validate_model(model):
			merge_model(model)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Perform basic model validations.')
	parser.add_argument('--id', help='problem ID (default: all problems in DETECTOR_ROOT)')
	args = parser.parse_args()

	load_envvars()

	if args.id is None:
		sys.exit('Mising --id') # TODO (for each file in dir...)
	else:
		main(args.id)
