import requests, csv, time
from collections import OrderedDict

# Each function uses a different service 

class Geocoder():

	"""Pings APIs and each function uses a different service"""

	def __init__(self, full_address=None, street='', city='', state='', zip='', google_key=None):
		self.full_address = full_address
		self.street = street
		self.city = city
		self.state = state
		self.zip = zip
		self.google_key = google_key or 'AIzaSyAH5jEajQVsB2ZrB5kZ3prps1TOjT9PIqE'


	def nominatim(self):
		"""Use Nominatim service: wiki.openstreetmap.org/wiki/Nominatim"""

		url = 'http://nominatim.openstreetmap.org/search'

		if self.full_address:
			url_args = {'q':self.full_address, 'format':'json'}
		else:
			url_args = {'street':self.street,
							'city':self.city,
							'state':self.state,
							'postalcode':self.zip,
							'format':'json'
							}

		r = requests.get(url, params=url_args)

		result = {}
		try:
			result['latitude'] = r.json()[0].get('lat')
			result['longitude'] = r.json()[0].get('lon')
			result['normalized_address'] = r.json()[0].get('display_name')
			result['precision'] = r.json()[0].get('class')
			result['service'] = 'OpenStreetMaps'
		except Exception, e:
			result['latitude'] = ''
			result['longitude'] = ''
			result['normalized_address'] = ''
			result['precision'] = 'ERROR: ' + str(e)
			result['service'] = 'OpenStreetMaps'

		return result


	def google_api(self):
		"""Use Datascient Toolkit, which is then based on open street maps"""

		url = 'https://maps.googleapis.com/maps/api/geocode/json'

		if self.full_address:
			url_args = {'address':self.full_address, 'key':self.google_key}
		else:
			url_args = {'address':', '.join([self.street, self.city, self.state, self.zip]), 
						'key':self.api_key}

		time.sleep(0.2) # pause for 1/5 of a second between each request
		r = requests.get(url, params=url_args)

		result = {}
		try:
			result['latitude'] = r.json()['results'][0].get('geometry').get('location').get('lat')
			result['longitude'] = r.json()['results'][0].get('geometry')['location']['lng']
			result['normalized_address'] = r.json()['results'][0].get('formatted_address')
			result['precision'] = r.json()['results'][0].get('geometry').get('location_type')
		except Exception, e:
			result['latitude'] = ''
			result['longitude'] = ''
			result['normalized_address'] = ''
			result['precision'] = 'ERROR: ' + str(e)
			result['service'] = 'GoogleMaps'

		return result



class csvLoader():

	"""Ingests a file as csv, prints out columns, then puts it through geocoding service"""

	def __init__(self, filename=None):
		self.filename = filename

	def show_columns(self):
		infile = csv.reader(open(self.filename, 'rU'))
		columns = infile.next()
		first_row = infile.next()

		return OrderedDict(zip(columns, first_row))

	def count_columns(self):
		infile = csv.reader(open(self.filename, 'rU'))
		return len(infile.next())

	def count_rows(self):
		infile = csv.reader(open(self.filename, 'rU'))
		return sum(1 for row in infile)

	def geocode_csv(self, outfilename='sample.csv', mapping=None):
		infile = csv.reader(open(self.filename, 'rU'))
		headers = infile.next()

		new_headers = headers + ['latitude', 'longitude', 'precision', 'service']

		outfile = csv.writer(open(outfilename, 'w'))
		outfile.writerow(new_headers)

		for row in infile:
			new_row = []
			try:
				full_address = row[int(mapping.get('Full Address'))]
			except:
				full_address = None
			try:
				street = row[int(mapping.get('Address'))]
			except:
				street = None
			try:
				city = row[int(mapping.get('City'))]
			except:
				city = None
			try:
				state = row[int(mapping.get('State'))]
			except:
				state = None
			try:
				zip = row[int(mapping.get('Zip'))]
			except:
				zip = None

			g = Geocoder(full_address=full_address, street=street, city=city, state=state, zip=zip)
			r = g.nominatim()
			new_row.extend(row)
			new_row.extend([r['latitude'], r['longitude'], r['precision'], r['service']])
			outfile.writerow(new_row)


		return None





class DataMapping():

	"""Opens a CSV of data column mapping"""

	def __init__(self, filename=None):
		self.filename = filename

	def lu_index(self):
		infile = csv.reader(open(self.filename, 'rU'))
		result = {}
		for row in infile:
			result[row[1]] = row[0]
		return result

	def lu_field(self):
		infile = csv.reader(open(self.filename, 'rU'))
		result = {}
		for row in infile:
			result[row[0]] = row[1]
		return result

	def dump_mapping(self, mapping):
		outfile = csv.writer(open(self.filename, 'w'))
		outfile.writerows(mapping)
		return None












