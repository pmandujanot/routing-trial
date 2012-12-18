"""Haversine formula for RoutingUC Test

See distance.__doc__ for credits.
"""
	
import math

def distance(origin, destination, radius=6371):
	"""Haversine formula
	Author: Wayne Dyck
	
	Source: http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
	"""
	lat1, lon1 = origin
	lat2, lon2 = destination
	
	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c

	return d