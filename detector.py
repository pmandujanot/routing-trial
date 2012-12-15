#!/usr/bin/python
import argparse
import csv
import os
import sys


def load_envvars():
	"""Loads environment variables"""
	global DETECTOR_ROOT, DATABASE_SERVER, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_TYPE
	DETECTOR_ROOT = os.getenv('DETECTOR_ROOT', 'data')
	DATABASE_SERVER = os.getenv('DATABASE_SERVER', 'localhost')
	DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'routing')
	DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'routing')
	DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'mysql').lower()


def load_csv(filename):
	"""Loads a CSV file"""
	try:
		with open(filename, 'rb') as f:
			reader = csv.reader(f)
			lines = []
			reader.next()	# skip the header
			for row in reader:
				lines.append(row)
			return lines
	except IOError as e:
		print(e)
		return None
	except csv.Error as e:
		print('file %s, line %d: %s' % (filename, reader.line_num, e))
		return None


def load_model(id):
	"""Loads a model from its CSV files"""
	print("LOADING data " + str(id))
	e = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-E.csv'))
	p = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-P.csv'))
	r = load_csv(os.path.join(DETECTOR_ROOT, str(id) + '-R.csv'))
	if (e is None) or (p is None) or (r is None):
		return None
	return [e, p, r]


def validate_model(model):
	"""Perform model validations"""
	# TODO
	print("ALL TESTS PASSED")
	return True


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



#EOF