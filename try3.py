import urllib2
from pattern.web import *

class parse:
	def __init__(self, url):
		self.url = url
		
	def	recipe(self, url):
		if self.url[11] == 'e':
			u = urllib2.urlopen(self.url)
			u = u.read()
			u = plaintext(u)

			recipe = u.split('\n')
			num = 0
			while num<len(recipe):
				text = recipe[num]
				recipe[num] = text.encode('ascii','ignore')
				num = num + 1


			cutting_num1 = recipe.index('Preparation')+3
			cutting_num2 = recipe.index('Exclusive Offers') - 1
			recipe = recipe[cutting_num1:cutting_num2]
		if self.url[11] == 'b':
			u = urllib2.urlopen(self.url)
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
			for i in range(len(recipe)):
				if recipe[i+1] == '' or '*':
					del recipe[i+1]

		return recipe
	def ingredients(self, url):
		url2 = urllib2.urlopen(self.url)
		

in_put = parse('http://www.bonappetit.com/recipe/pan-roasted-chicken-with-pineapple-chile-glaze')
print in_put.recipe('http://www.bonappetit.com/recipe/pan-roasted-chicken-with-pineapple-chile-glaze')