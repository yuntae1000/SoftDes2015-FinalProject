import urllib2
import json
import string

class find_stores():
	def __init__(self, my_key):
		self.my_key = my_key
		my_key = 'AIzaSyDJm9wnT8bVC1nxJ61OKwcMdkwDpxakcWg'
		pass

	def get_location(self, origin):
		self.origin = origin
		search_origin = origin.split(' ')
		origin = '+'.join(search_origin)
		my_key = self.my_key
		response1 = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address='+origin+'&key='+my_key).read()
		response1 = json.loads(response1)
		location = response1['results'][0]['geometry']['location']
		latitude, longitude = location['lat'], location['lng']
		return latitude, longitude

	def search_stores(self, radius):
		location = self.get_location(self.origin)
		a = str(location[0])
		b = str(location[1])
		self.radius = radius
		c = str(radius)
		my_key = self.my_key
		response2 = urllib2.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+a+','+b+'&radius='+c+'&types=grocery_or_supermarket&key='+my_key).read()
		response2 = json.loads(response2)
		return response2

		#ADD DB - Extracting the Stores
		#Give me the data; name, location(lat, lng), opening hours
	"""
	def near_you(self):
		location = self.get_lacation(self.origin)
		a = str(location[0])
		b = str(location[1])
		c = destination1|destination2
		response3 = urllib2.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+a+','+b+'&destinations='+c+'&key='+my_key).read()
		response3 = fson.loads(response3)
	"""

a = find_stores('AIzaSyDJm9wnT8bVC1nxJ61OKwcMdkwDpxakcWg')
b = a.get_location('4 Charles St, Boston, MA')
c = a.search_stores(1000)
print c