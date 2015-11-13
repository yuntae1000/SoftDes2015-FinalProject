import urllib2
import json
API= "330d2c5996a36203ad2247c1e705b4bb"
searchdish = "kimchi"
response = urllib2.urlopen('http://food2fork.com/api/search?key='+API+'&q=thai').read()
jsondata=json.loads(response)
websites=[u'Closet Cooking',u'All Recipes',u'Epicurious']
recipe_lists=[]
f2furl_ingredients=[]

for urls in filter(lambda x: x[u'publisher'] in websites, jsondata[u'recipes']):
	print urls
	recipe_lists.append(urls)
	#to get ingredients from f2f urls, get the f2f urls in lists
	f2furl_ingredients.append(str(urls[u'f2f_url']))
	# print jsondata[u'recipes'][urls][u'source_url']
	#source_url.append(url)
#print json.dumps(response)
print recipe_lists
print f2furl_ingredients

print len(recipe_lists)
