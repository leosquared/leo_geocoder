import os
from celery import Celery, current_task
from Geocoder import Geocoder, csvLoader, DataMapping

app = Celery()

# Celery config
app.conf.update(BROKER_URL=os.environ.get('REDISTOGO_URL', 'redis://localhost:6379/0'),
                CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', 'redis://localhost:6379/0'),
				CELERY_TASK_SERIALIZER='json'
				)


@app.task
def hello(filename):
	f = open(filename, 'w')
	f.write('hello, world')
	f.close()

@app.task 
def file_geocode(input_file, mapping_file, geocoded_file, form_values):
	
	# Create mapping file from CSV and HTML form input
	myCSV = csvLoader(input_file)
	myMapping = DataMapping(filename=mapping_file)
	mapping = []
	for i in range(myCSV.count_columns()):
		try:
		    form_value = form_values.get(str(i))
		except:
			form_value = ''
		mapping.append([i, form_value])
	myMapping.dump_mapping(mapping)

	myCSV.geocode_csv(mapping=myMapping.lu_index(), outfilename=geocoded_file)

	# # read input file, use map index
	# mapping_index = myMapping.lu_index()
	# infile = csv.reader(open(input_file, 'rU'))
	# headers = infile.next()
	# new_headers = headers + ['latitude', 'longitude', 'precision', 'service']
	# outfile = csv.writer(open(geocoded_file, 'w'))
	# outfile.writerow(new_headers)

	# counter = 0
	# for row in infile:
	# 	new_row = []
	# 	try:
	# 		full_address = row[int(mapping_index.get('Full Address'))]
	# 	except:
	# 		full_address = None
	# 	try:
	# 		street = row[int(mapping_index.get('Address'))]
	# 	except:
	# 		street = None
	# 	try:
	# 		city = row[int(mapping_index.get('City'))]
	# 	except:
	# 		city = None
	# 	try:
	# 		state = row[int(mapping_index.get('State'))]
	# 	except:
	# 		state = None
	# 	try:
	# 		zip = row[int(mapping_index.get('Zip'))]
	# 	except:
	# 		zip = None

	# 	g = Geocoder(full_address=full_address, street=street, city=city, state=state, zip=zip)
	# 	r = g.nominatim()
	# 	new_row.extend(row)
	# 	new_row.extend([r['latitude'], r['longitude'], r['precision'], r['service']])
	# 	outfile.writerow(new_row)
	# 	counter += 1

	# 	current_task.update_state(state='PROGRESS', meta={'current':counter, 'total':myCSV.count_rows()})

	# return None
