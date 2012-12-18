
def merge_data(originalSchoolsList, newSchoolsList, dbManager):
	
	#For each new school add it to the original school list
	for newSchool in newSchoolsList:
		#Get the schools with the same id
		oldSchooldWithSameID = [x for x in originalSchoolsList if x.s_id == newSchool.s_id]

		#If there's not another school with the same ID, we simply append the new school. If there is another school, we must merge them:
		if len(oldSchooldWithSameID) == 0:
			originalSchoolsList.append(newSchool)

		elif len(oldSchooldWithSameID) == 1:
			merge_schools(originalSchoolsList, oldSchooldWithSameID[0], newSchool, dbManager)

		else:
			raise Exception("Duplicate School ID (%i) on the Database" % (newSchool.s_id))


def merge_schools(originalSchoolsList, oldSchool, newSchool, dbManager):
	#Transfer the routes from the old school to the new one.
	merge_routes(oldSchool, newSchool, dbManager)

	#Delete the old school from the original list (given that the ids are the same, this will cause an update of the school entity on the database)
	originalSchoolsList.remove(oldSchool)

	#Add the new school:
	originalSchoolsList.append(newSchool)


def merge_routes(oldSchool, newSchool, dbManager):
	#From the old school add all the routes to the new school. If there are two routes with the same ID, the new one will replace the old one.
	for oldRouteID in oldSchool.routes.keys():
		if oldRouteID not in newSchool.routes.keys():
			newSchool.routes[oldRouteID] = oldSchool.routes[oldRouteID]
		else:
			#If the route of the oldschool is in the new school, then we must delete it and remove it from the database:
			dbManager.delete_route(oldSchool.routes[oldRouteID])





