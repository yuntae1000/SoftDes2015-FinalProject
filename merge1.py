import urllib2
import json
import html2text
import string
import sys
import math
from pattern.web import *
reload(sys)
sys.setdefaultencoding('utf8')
socket.timeout


API= "330d2c5996a36203ad2247c1e705b4bb"
#User Input the Value
searchdish = "donut"

response = urllib2.urlopen('http://food2fork.com/api/search?key='+API+'&q='+searchdish).read()
jsondata=json.loads(response)
websites=[u'Closet Cooking',u'All Recipes',u'Epicurious', u'Bon Appetit']
recipe_lists=[]
f2furl_ingredients=[]
ingredients_lists=[]


def getRecipeurl():
	for urls in filter(lambda x: x[u'publisher'] in websites, jsondata[u'recipes']):
		recipe_lists.append(urls)
		#to get ingredients from f2f urls, get the f2f urls in lists
		f2furl_ingredients.append(str(urls[u'f2f_url']))
		uurl = recipe_lists[0]['source_url']
		if uurl[7] == 'a':
			uurl = uurl[:7] + 'www.' + uurl[7:]
		return uurl

def getIngredients(index):
	response2=urllib2.urlopen(f2furl_ingredients[index]).read()
	html=html2text.html2text(response2)
	#print html
	a=string.find(html,'#### Ingredients')
	b=string.find(html,'#### Directions')
	ingredient=html[a:b-1]
	ingredients_lists.append([ingredient])

class parse:
	def __init__(self):
		pass

	def allrecipes(self, url):

		recipe = []
		html = urllib2.urlopen(url).read()
		a = html.split("""<li class="step" ng-class="{'finished': stepIsActive0}" ng-click="stepIsActive0 = !stepIsActive0"><span class="recipe-directions__list--item">""")
		b = a[1].split("""<ol class="list-numbers recipe-directions__list recipeNotes ng-hide" ng-show="itemNote" ng-cloak>""")
		c = b[0].split("""<li class="step" ng-class="{'finished': stepIsActive""")
		for i in range(len(c)):
			if i==0 :
				x = c[0].split('<')
				recipe.append(x[0])
			else :
				x = c[i].split('>')
				y = x[2].split('<')
				recipe.append(y[0])
		return recipe

	def closetcooking(self, url):
		recipe = []
		html = urllib2.urlopen(url).read()
		text = plaintext(html)
		a = text.split('directions')
		b = a[1].split('\n\n')
		c = b[1].split('\n')
		for i in range(len(c)):
			if len(c[i]) > 0:
				if c[i][0]=='*':
					d = c[i][2:]
					recipe.append(d)
		return recipe
		
	def epicurious(self, url):
		u = urllib2.urlopen(url)
		u = u.read()
		u = plaintext(u)
		recipe = u.split('\n')
		num = 0
		while num<len(recipe):
			text = recipe[num]
			recipe[num] = text.encode('ascii','ignore')
			num = num + 1
		cutting_num1 = recipe.index('Preparation')+3
		cutting_num2 = recipe.index('Nutritional Info') - 1
		recipe = recipe[cutting_num1:cutting_num2]
		recipe = [x for x in recipe if x != '']
		recipe = [x for x in recipe if x != '*']
		return recipe

	def bonappetit(self, url):
		u = urllib2.urlopen(url)
		u = u.read()
		u = plaintext(u)
		recipe = u.split('\n')		
		num = 0
		while num<len(recipe):
			text = recipe[num]
			recipe[num] = text.encode('ascii','ignore')
			num = num + 1		
		cutting_num1 = recipe.index('Preparation')+3
		cutting_num2 = recipe.index('See More') - 6
		recipe = recipe[cutting_num1:cutting_num2]
		recipe = [x for x in recipe if x != '']
		recipe = [x for x in recipe if x != '*']
		return recipe

	def	recipe(self, url):
		if url[11] == 'a':
			recipe = self.allrecipes(url)
		if url[11] == 'c':	
			recipe = self.closetcooking(url)
		if url[11] == 'e':
			recipe = self.epicurious(url)
		if url[11] == 'b':
			recipe = self.bonappetit(url)
		return recipe

	def servings(self, url):
		if url[11] == 'b':
			u = urllib2.urlopen(url)
			u = u.read()
			u = plaintext(u)
			recipe = u.split()
			servings = recipe.index('Servings:')
			text = recipe[servings+1]
			servings = text.encode('ascii', 'ignore')
			return float(servings)
		if url[11] == 'e':
			u = urllib2.urlopen(url)
			u = u.read()
			u = plaintext(u)
			recipe = u.split()
			servings = recipe.index('YieldMakes')
			text = recipe[servings+1]
			servings = text.encode('ascii', 'ignore')
			return float(servings)
		if url[11] == 'a':
			u = urllib2.urlopen(url)
			u = u.read()
			recipe = u.split()
			servings = recipe.index('itemprop="recipeYield"')
			text = recipe[servings+1]
			servings = text.encode('ascii', 'ignore')
			servings = servings[8:]
			servings = servings.strip(string.punctuation)
			return float(servings)

class ready_for_cost():
	def __init__(self):
		pass

	# Make the fakelist which can be used easily
	def make_fakelist(self, ing_str):
		self.ing_str = ing_str
		fakelist = ing_str.split()
		num = 0
		while num<len(fakelist):
				text = fakelist[num]
				fakelist[num] = text.encode('ascii','ignore')
				num = num + 1
		fakelist = [x for x in fakelist if x != ',']
		
		return fakelist

	#Make the amount(float) list
	def amount(self, ing_str):
		fakelist = self.make_fakelist(ing_str)
		amount_list = []
		numberset = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
		for i in range(len(fakelist)):
			if fakelist[i] == '*':
				for j in range(len(numberset)):
					if fakelist[i+1][0] == numberset[j]:
						amount_list.append(fakelist[i+1])
		for i in range(len(amount_list)):
			if '/' in amount_list[i]:
				position = amount_list[i].index('/')
				numerator = float(amount_list[i][:position])
				denominator = float(amount_list[i][position+1:])
				amount_list[i] = numerator/denominator*m_people/n_people
			else:
				amount_list[i] = float(amount_list[i])
				amount_list[i] = amount_list[i]*m_people/n_people
		amount_list = [x for x in amount_list if x != '']
		return amount_list

	#Make the unit list
	def unit(self, ing_str):
		fakelist = self.make_fakelist(ing_str)
		unit_list = []
		unitset = ['cup', 'cups', 'tablespoon', 'tablespoons', 'pound', 'jars', 'teaspoon', 'teaspoons', 'ounce', 'ounces', 'dessertspoon', 'dessertspoons', 'dash', 'gallon', 'shot', 'liter', 'l', 'mililiter', 'ml']
		numberset = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
		for i in range(len(fakelist)):
			for j in range(len(numberset)):
				if fakelist[i][0] == numberset[j]:
					if fakelist[i-1] == '*':
						if fakelist[i+1] not in unitset:
							unit_list.append('no unit')
						else:
							for k in range(len(unitset)):
								if fakelist[i+1] == unitset[k]:
									unit_list.append(unitset[k])
		unit_list = [x for x in unit_list if x != '']
		return unit_list

	#Make the name of ingredients list
	def name(self, ing_str):
		fakelist = self.make_fakelist(ing_str)
		name_list = []
		unitset = ['cup', 'cups', 'tablespoon', 'tablespoons', 'pound', 'jars', 'teaspoon', 'teaspoons', 'ounce', 'ounces', 'dessertspoon', 'dessertspoons', 'dash', 'gallon', 'shot', 'liter', 'l', 'mililiter', 'ml']
		numberset = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
		for i in range(len(fakelist)):
			if fakelist[i] == '*':
				if fakelist[i+1][0] in numberset:
					if fakelist[i+2] in unitset:
						j = i+3
						naming=''
						while j<len(fakelist) and fakelist[j] != '*':
							naming += fakelist[j] + ' '
							j +=1
						name_list.append(naming)
					elif fakelist[i+2] not in unitset:
						j = i+2
						naming=''
						while j<len(fakelist) and fakelist[j] != '*':
							naming += fakelist[j] + ' '
							j +=1
						name_list.append(naming)
				elif fakelist[i+1][0] not in numberset:
					j = i+1
					naming = ''
					while j<len(fakelist) and fakelist[j] != '*':
						naming += fakelist[j] + ' '
						j +=1
					name_list.append(naming)
		name_list = [x for x in name_list if x != '']
		return name_list

used_url = getRecipeurl()
for i in range(len(f2furl_ingredients)):
	getIngredients(i)
final_ingre = ingredients_lists[0]
print final_ingre
final_ingre = final_ingre[0]


url = used_url
Parse = parse()
recipe= Parse.recipe(url)
print recipe
howmany = Parse.servings(url)

n_people = howmany
#User Input the Value
m_people = 8 #the number of invited people

a = ready_for_cost()
list_amount = a.amount(final_ingre)
list_unit = a.unit(final_ingre)
list_name = a.name(final_ingre)
print list_amount
print list_unit
print list_name



