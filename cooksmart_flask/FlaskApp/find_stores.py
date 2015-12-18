import urllib2
import json
import string

class find_stores():
	def __init__(self):
		self.my_key = 'AIzaSyApIG8MCc27QujOSL2JCtKicVJdTQsSVkY'
		self.datalist2=[]
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
		response2 = response2['results']
		datalist = dict()
		
		for i in range(len(response2)):
			datalist[response2[i]['name']] = response2[i]['geometry']['location']['lat'], response2[i]['geometry']['location']['lng']
			
			self.datalist2.append(response2[i]['name'])
        #ADD DB PART HERE- Extracting the Stores

		return datalist

	def near_you(self):
		my_key = self.my_key
		location = self.get_location(self.origin)
		a = str(location[0])
		b = str(location[1])
		stores = self.search_stores(self.radius)
		name_list = stores.keys()
		location_list = stores.values()
		for i in range(len(location_list)):
			location_list[i] = str(location_list[i][0]) + ',' + str(location_list[i][1])
		c = '|'.join(location_list)
		response3 = urllib2.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+a+','+b+'&destinations='+c+'&key='+my_key).read()
		response3 = json.loads(response3)
		response3 = response3['rows'][0]['elements']
		datalist = {}
		for i in range(len(response3)):
			datalist[name_list[i]] = response3[i]['distance']['text'], response3[i]['duration']['text']
		return datalist

#'AIzaSyDJm9wnT8bVC1nxJ61OKwcMdkwDpxakcWg'
