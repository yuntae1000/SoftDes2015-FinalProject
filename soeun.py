import urllib2
import sys
from pattern.web import *
reload(sys)
sys.setdefaultencoding('utf8')

def iherb_search(ingredient):
    iherb_ingredient = ingredient.replace(" ","+")
    iherb_url = 'http://www.iherb.com/search?kw='+iherb_ingredient+'#p=1'
    iherb_html = URL(iherb_url).download()
    iherb_text = plaintext(iherb_html)

    a = iherb_text.split('Relevance Best Selling Customer Rating Price: Low to High Price: High to Low On Sale New Arrivals Heaviest Lightest')
    b = a[1].split('\n')
    del b[:4]
    
    c=[]
    
    for i in range(len(b)):
        if b[i] == '':
            pass
        else:
            c.append(b[i])

    ing_list = []

    for i in range(len(c)):
        if i%3 == 0 or i%3 == 2:
            ing_list.append(c[i])

    
    ingredient_list = []


    for i in range(3):
        x=[]
        a = ing_list[2*i].split(',')
        b = len(a)
        amount = a[b-1]
        del a[b-1]
        name = ''
        for j in range(len(a)):
            name += a[j]
        x.append(name.lower())
        b = amount.split(' ')
        x.append(b[1])
        x.append(b[2].lower())
        x.append(ing_list[2*i+1].lower())
        ingredient_list.append(x)

    return ingredient_list

    # result = [ingredient, amount, unit, price] * 3




def walmart_search(ingredient):
    walmart_ingredient = ingredient.replace(" ","%20")
    walmart_url = 'http://www.walmart.com/search/?query='+walmart_ingredient    
    walmart = []

    walmart_html = urllib2.urlopen(walmart_url).read()
    walmart_text = plaintext(walmart_html)
    

    a = walmart_text.split('Sort Best match Best sellers Price: low to high Price: high to low Highest rating New')
    b = a[1].split('\n')
    

    for i in range(len(b)):
        if b[i] == '':
            pass
        elif b[i][0] == '*':
            pass
        elif '/' in b[i] or '(' in b[i]:
            pass
        elif b[i] == 'New':
            pass
        else:
            walmart.append(b[i])
    
    ingredient_list = []

    for i in range(3):
        x = []
        a = walmart[2*i].split(',')
        x.append(a[0].lower())
        b = a[1].split(' ')
        x.append(b[1].lower())
        x.append(b[2].lower())
        x.append(walmart[2*i+1].lower())
        ingredient_list.append(x)


    return ingredient_list
    # result = [[ingredient, amount, unit, price]*3]



def produce_search(ingredient):
    produce_url = 'http://www.foodcoop.com/produce'
    produce_html = urllib2.urlopen(produce_url).read()
    produce_text = plaintext(produce_html)
    produce = produce_text.split('\n')

    for i in range(len(produce)):
        if produce[i] == 'Click on any column heading to sort by that column':
            a=i

    for i in range(len(produce)):
        if produce[i] == 'In this section':
            b=i

    produce = produce[a+3:b-1]
    produce_1 = []

    for i in range(len(produce)):
        a = produce[i].split('$')
        produce_1.append(a[0])
        produce_1.append(a[1])

    for i in range(len(produce_1)/2):
        if '-' in produce_1[2*i]:
            a = produce_1[2*i].find('-')
            produce_1[2*i] = produce_1[2*i][:a]
        produce_1[2*i+1] = '$'+produce_1[2*i+1]

    ing_list = []

    for i in range(len(produce_1)/2):
        x = []
        b = produce_1[2*i].lower()
        if 'per pound' in produce_1[2*i+1]:
            a = produce_1[2*i+1].find('per pound')
            x.append(b)
            x.append('1')
            x.append('pound')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)
        elif 'per bunch' in produce_1[2*i+1]:
            a = produce_1[2*i+1].find('per bunch')
            x.append(b)
            x.append('1')
            x.append('bunch')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)
        elif 'each' in produce_1[2*i+1]:
            a = produce_1[2*i+1].find('each')
            x.append(b)
            x.append('1')
            x.append('each')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)

    ingredient_list = []
    
    for i in range(len(ing_list)):
        if ingredient in ing_list[i][0]:
            ingredient_list.append(ing_list[i])

    return ingredient_list




def unify_units(ingredient_list):
    unit = ['cup','tablespoon','teaspoon','pound','lb']
    unify = [80, 0.5, 0.25, 16, 16, 0.03, 0.03]

    for i in range(len(ingredient_list)):
        for j in range(len(unit)):
            if 'fl' in ingredient_list[i][2]:
                ingredient_list[i][2] = 'oz'
            elif 'fl oz' in ingredient_list[i][1]:
                a = ingredient_list[i][1].find('fl oz')
                b = ingredient_list[i][1][:a-1]+'oz'
                c = b.replace(' ','')
                ingredient_list[i][1] = c
            elif unit[j] in ingredient_list[i][2]:
                ingredient_list[i][1] = ingredient_list[i][1]*unify[j]
                ingredient_list[i][2] = 'oz'

    return ingredient_list




def unify_recipe_unit(recipe_amount, recipe_unit):
    unit = ['oz','ounce''cup','tablespoon','teaspoon','pound','lb']
    unify = [1, 1, 80, 0.5, 0.25, 16, 16, 0.03, 0.03]
    for i in range(len(recipe_unit)):
        for j in range(len(unit)):
            if unit[j] in recipe_unit[i]:
                recipe_amount[i] = recipe_amount[i] * unify[j]
                recipe_unit[i] = 'oz'

    return [recipe_amount, recipe_unit]




def compare_amount(ingredient_list, recipe_amount, recipe_unit, recipe_name):
    a = [ingredient_list[0][3],ingredient_list[1][3],ingredient_list[2][3]]
    b = a.sort()
    c = []
    for j in range(3):
        for i in range(3):
            if ingredient_list[i][2]==b[j]:
                c.append(i)

    if recipe_unit == 'oz' and ingredient_list[[c[0]][2]] == 'oz':
        if recipe_amount < ingredient_list[[c[0]][1]] :
            return ingredient_list[c[0]]
        elif ingredient_list[[c[1]][3]] == 'In stores only':
            return ingredient_list[c[0]]
        elif recipe_amount < ingredient_list[[c[1]][1]] and ingredient_list[[c[1]][1]] < recipe_amount*2 :
            return ingredient_list[c[1]]
        elif ingredient_list[[c[2]][3]] == 'In stores only':
            return ingredient_list[c[1]]
        elif recipe_amount < ingredient_list[[c[2]][1]] and ingredient_list[[c[2]][1]] < recipe_amount*2 :
            return ingredient_list[c[2]]
        elif recipe_amount < ingredient_list[[c[2]][1]] and ingredient_list[[c[2]][1]] > recipe_amount*2 :
            return ingredient_list[c[1]]
        elif recipe_amount > ingredient_list[[c[2]][1]] :
            return ingredient_list[c[2]]
        else:
            return ingredient_list[c[0]] # mark the number

    else:
        return ingredient_list[c[0]] # mark the number
        



def ingredients_search(ingredient, amount):
    walmart_prices = [walmart_search(ingredient)[0][3],walmart_search(ingredient)[1][3],walmart_search(ingredient)[2][3]]
    a = walmart_prices.sort()
    iherb_prices = [iherb_search(ingredient)[0][3],iherb_search(ingredient)[1][3],iherb_search(ingredient)[2][3]]
    if len(produce_search(ingredient)) != 0:
        return produce_search(ingredient_list)
    elif 'In stores only' not in walmart_prices:
        return walmart_search(ingredient)
    elif a[2] == 'In stores only' and a[1] != 'In stores only':
        return walmart_search(ingredient)
    elif min(a[0],iherb_prices[0],iherb_prices[1],iherb_prices[2]) in a :
        return walmart_search(ingredient)
    elif min(a[0],iherb_prices[0],iherb_prices[1],iherb_prices[2]) in iherb_prices :
        return iherb_search(ingredient)





#ingredients_search('butter')
print produce_search('carrot')
print iherb_search('black pepper')
print walmart_search('butter')


