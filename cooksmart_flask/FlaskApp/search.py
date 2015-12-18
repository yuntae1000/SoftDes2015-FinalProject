import urllib2
import json
import html2text
import string
API= "330d2c5996a36203ad2247c1e705b4bb"
searchdish = "pizza"
response = urllib2.urlopen('http://food2fork.com/api/search?key='+API+'&q='+searchdish).read()

jsondata=json.loads(response)
print jsondata
websites=[u'Closet Cooking',u'All Recipes',u'Epicurious']
recipe_lists=[]
f2furl_ingredients=[]
ingredients_lists=[]

def getRecipeurl():
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

def getIngredients(index):

	response2=urllib2.urlopen(f2furl_ingredients[index]).read()
	#print response2
	html=html2text.html2text(response2)
	#print html
	a=string.find(html,'#### Ingredients')
	b=string.find(html,'#### Directions')
	ingredient=html[a:b-1]
	ingredients_lists.append([ingredient])
	#jsondata2=json.loads(response2)
	#print jsondata2
	#print json.loads(response2)


getRecipeurl()
#print type(f2furl_ingredients[0])
for i in range(len(f2furl_ingredients)):
	getIngredients(i)
print ingredients_lists
print "ingredien bibim"
print ingredients_lists[0]