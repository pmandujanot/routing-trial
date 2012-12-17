from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData, ForeignKey, select # external dependencies (v0.7.4)
from sqlalchemy.sql import and_, or_, not_


def get_db_engine(server, username, password, type):
	"""Returns DB engine"""
	#TODO: Missing database name, assuming same as username
	if type in ["mysql", "posgresql", "sqlite"]:
		return create_engine("{0}://{1}:{2}@{3}/{4}".format(type, username, password, server, username), echo=False)
	else:
		#return create_engine('sqlite:///:memory:', echo=True)
		raise Exception("Unsupported DB type " + str(type))


def initialize_metadata(engine):
	"""Returns DB metadata and creates tables if they do not exist"""
	metadata = MetaData()
	bus_stop = Table('paradero', metadata,
		Column('stop_id', Integer, primary_key=True, autoincrement=False),
		Column('lat', Float),
		Column('lng', Float),
		Column('name', String(255)),
		Column('p_1', Integer),
		Column('p_2', Integer),
		Column('p_3', Integer),
		Column('p_4', Integer),
		Column('bucket', String(255), primary_key=True)
		)
	school = Table('escuela', metadata,
		Column('school_id', Integer, primary_key=True, autoincrement=False),
		Column('lat', Float),
		Column('lng', Float),
		Column('name', String(255)),
		Column('c_1', Integer),
		Column('c_2', Integer),
		Column('c_3', Integer),
		Column('c_4', Integer),
		Column('bucket', String(255), primary_key=True)
		)
	route = Table('ruta', metadata,
		Column('stop_id', None, ForeignKey('paradero.stop_id'), primary_key=True),
		Column('route_id', Integer, primary_key=True, autoincrement=False),
		Column('school_id', None, ForeignKey('escuela.school_id')),
		Column('order', Integer),
		Column('bucket', String(255), primary_key=True)
		)
	metadata.create_all(engine)
	return metadata


def upsert_model(engine, metadata, model, bucket):
	"""Updates or inserts the model elements into the DB"""
	conn = engine.connect()
	try:
		table = metadata.tables['paradero']
		for bus_stop in model.bus_stops.values():
			# check if record already exists
			s = select([table], and_(table.c.stop_id == bus_stop.bus_stop_id, table.c.bucket == bucket))
			if conn.execute(s).rowcount > 0:
				action = table.update().where(and_(table.c.stop_id == bus_stop.bus_stop_id, table.c.bucket == bucket))
			else:
				action = table.insert()

			# save
			conn.execute(
				action,
				stop_id = bus_stop.bus_stop_id,
				lat = bus_stop.location[0],
				lng = bus_stop.location[1],
				name = bus_stop.name,
				p_1 = bus_stop.c[0],
				p_2 = bus_stop.c[1],
				p_3 = bus_stop.c[2],
				p_4 = bus_stop.c[3],
				bucket = bucket
				)

		table = metadata.tables['escuela']
		for school in model.schools.values():
			# check if record already exists
			s = select([table], and_(table.c.school_id == school.school_id, table.c.bucket == bucket))
			if conn.execute(s).rowcount > 0:
				action = table.update().where(and_(table.c.school_id == school.school_id, table.c.bucket == bucket))
			else:
				action = table.insert()

			# save
			conn.execute(
				action,
				school_id = school.school_id,
				lat = school.location[0],
				lng = school.location[1],
				name = school.name,
				c_1 = school.c[0],
				c_2 = school.c[1],
				c_3 = school.c[2],
				c_4 = school.c[3],
				bucket = bucket
				)

		table = metadata.tables['ruta']
		for route in model.routes.values():
			for r in route:
				# check if record already exists
				s = select([table], and_(table.c.route_id == r.route_id, table.c.bucket == bucket))
				if conn.execute(s).rowcount > 0:
					action = table.update().where(and_(table.c.route_id == r.route_id, table.c.bucket == bucket))
				else:
					action = table.insert()

				# save
				conn.execute(
					action,
					stop_id = r.bus_stop_id,
					route_id = r.route_id,
					school_id = r.alloc_id,
					order = r.order,
					bucket = bucket
					)
	finally:
		conn.close()
