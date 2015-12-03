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
        x.append(name)
        x.append(amount[1:])
        x.append(ing_list[2*i+1])
        ingredient_list.append(x)

    return ingredient_list

    # result = [ingredient, amount, price] * 3




def walmart_search(ingredient):
    walmart_ingredient = ingredient.replace(" ","%20")
    walmart_url = 'http://www.walmart.com/search/?query='+walmart_ingredient    
    walmart = []

    walmart_html = urllib2.urlopen(walmart_url).read()
    walmart_text = plaintext(walmart_html)

    a = walmart_text.split('Sort Best match Best sellers Price: low to high Price: high to low Highest rating New')
    b = a[1].split('\n')
    print b

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

    for i in range(len(ingredient_list/2)):
        x = []
        a = walmart[2*i].split(',')
        x.append(a[0])
        x.append(a[1][1:])
        x.append(walmart[2*i+1])
        ingredient_list.append(x)


    return ingredient_list
    # result = [[ingredient, amount, price]*3]


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
            x.append('pound')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)
        elif 'per bunch' in produce_1[2*i+1]:
            a = produce_1[2*i+1].find('per bunch')
            x.append(b)
            x.append('bunch')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)
        elif 'each' in produce_1[2*i+1]:
            a = produce_1[2*i+1].find('each')
            x.append(b)
            x.append('each')
            x.append(produce_1[2*i+1][:a-1])
            ing_list.append(x)

    ingredient_list = []
    
    for i in range(len(ing_list)):
        if ingredient in ing_list[i][0]:
            ingredient_list.append(ing_list[i])

    return ingredient_list



    #return ingredient_list
    #'each, bunch, pound'
    # result = [ingredient, price+amount]


def compare_amount():
    'jk'


def ingredients_search(ingredient, amount):
    if len(produce_search(ingredient)) != 0:
        'dfd'
    #elif walmart_search(ingredient)





    'In stores only'



#ingredients_search('butter')
#print produce_search('carrot')
#print iherb_search('black pepper')
#print walmart_search('butter')


