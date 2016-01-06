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
		response2 = response2['results']
		datalist = dict()
		for i in range(len(response2)):
			datalist[response2[i]['name']] = response2[i]['geometry']['location']['lat'], response2[i]['geometry']['location']['lng']
		
        #ADD DB PART HERE- Extracting the Stores
        #^^There are ways to start writing new functions and leaving them as placeholders
        #you can define a funtion that you want to write (e.g., that accesses a DB)
        #and then you can just have the command 'pass' in the body of the funtion.
        #it woun't do anything and you return to write functional code later.

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

a = find_stores('AIzaSyDJm9wnT8bVC1nxJ61OKwcMdkwDpxakcWg')
b = a.get_location('4 Charles St, Boston, MA')
c = a.search_stores(500)
d = a.near_you()
print c
print d
#for readability, consider using more descriptive variable names.
#also consider putting the final lines under an if __name__ == '__main__':