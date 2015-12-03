import urllib2
from pattern.web import *

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
		print recipe
		cutting_num1 = recipe.index('Preparation')+3
		cutting_num2 = recipe.index('Exclusive Offers') - 1
		recipe = recipe[cutting_num1:cutting_num2]
		recipe = [x for x in recipe if x != '']
		recipe = [x for x in recipe if x != '*']
		print "printing recipe", recipe
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
			print "epicurious"
		if url[11] == 'b':
			recipe = self.bonappetit(url)
		return recipe
		
url = 'http://www.epicurious.com/recipes/food/views/Bibimbap-at-Home-51140460'
Parse = parse()
#in_put = parse('http://www.bonappetit.com/recipe/pan-roasted-chicken-with-pineapple-chile-glaze')
recipe= Parse.recipe(url)
print recipe

#in_put = 'http://www.bonappetit.com/recipe/pan-roasted-chicken-with-pineapple-chile-glaze'
#print parse.recipe('http://www.bonappetit.com/recipe/pan-roasted-chicken-with-pineapple-chile-glaze')		
