import requests, csv, time

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
		result['latitude'] = r.json()[0].get('lat')
		result['longitude'] = r.json()[0].get('lon')
		result['normalized_address'] = r.json()[0].get('display_name')
		result['precision'] = r.json()[0].get('class')
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
		result['latitude'] = r.json()['results'][0].get('geometry').get('location').get('lat')
		result['longitude'] = r.json()['results'][0].get('geometry')['location']['lng']
		result['normalized_address'] = r.json()['results'][0].get('formatted_address')
		result['precision'] = r.json()['results'][0].get('geometry').get('location_type')

		return result



class csvLoader():

	"""Ingests a file as csv, prints out columns, then puts it through geocoding service"""

	def __init__(self, filename=None):
		self.filename = filename

	def show_columns(self):
		infile = csv.reader(open(self.filename))
		columns = infile.next()
		first_row = infile.next()
		return {'columns':columns, 'first_row':firts_row}











