import os
from celery import Celery
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
	myCSV = csvLoader(input_file)
	myMapping = DataMapping(filename=mapping_file)
	mapping = []
	for i in range(myCSV.count_columns()):
	    form_value = form_values.get(str(i))
	    mapping.append([i, form_value])
	myMapping.dump_mapping(mapping)
	myCSV.geocode_csv(mapping=myMapping.lu_index(), outfilename=geocoded_file)
