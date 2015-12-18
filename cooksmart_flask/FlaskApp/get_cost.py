# the pasted recipe source that Jake gives
kimchi = [u'#### Ingredients:\n\n  * 1/2 cup reduced-sodium soy sauce\n  * 1/3 cup finely grated Asian pear with juices\n  * 2 scallions, thinly sliced\n  * 2 garlic cloves, minced\n  * 1 tablespoon raw or brown sugar\n  * 2 teaspoons grated peeled ginger\n  * 1 pound thinly sliced (1/8") boneless beef rib-eye steak or short ribs\n  * 3 tablespoons toasted sesame oil, divided\n  * 8 cups steamed sushi rice or mixed grain rice (from 2 1/2 cups dry rice)\n  * Bibimbap Mix-Ins (\n  * , \n  * , \n  * , \n  * , \n  * , \n  * , \n  * , and \n  * )\n  * 8 fried eggs\n  * Kimchi\n\n']
pasta = [u'#### Ingredients:\n\n  * 1 pound dry ziti pasta\n  * 1 onion, chopped\n  * 1 pound lean ground beef\n  * 2 (26 ounce) jars spaghetti sauce\n  * 6 ounces provolone cheese, sliced\n  * 1 1/2 cups sour cream\n  * 6 ounces mozzarella cheese, shredded\n  * 2 tablespoons grated Parmesan cheese\n\n']
kimchi2 = kimchi[0]
pasta2 = pasta[0]

n_people = 4 #in the recipe
m_people = 8 #the number of invited people



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
		return name_list


a = ready_for_cost()
b = a.amount(kimchi2)
c = a.unit(kimchi2)
e = a.name(kimchi2)
print b
print c
print e

