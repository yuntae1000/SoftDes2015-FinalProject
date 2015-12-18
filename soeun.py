import urllib2
import sys
from pattern.web import *
reload(sys)
sys.setdefaultencoding('utf8')
socket.timeout


def iherb_search(ingredient):
    """
    input = str(ingredienet)
    output = [ [ingredient, amount, unit, price] * 3 ]
    """

    iherb_ingredient = ingredient.replace(" ","+")
    iherb_url = 'http://www.iherb.com/search?kw='+iherb_ingredient+'#p=1'
    iherb_html = URL(iherb_url).download()
    iherb_text = plaintext(iherb_html)

    a = iherb_text.split('Relevance Best Selling Customer Rating Price: Low to High Price: High to Low On Sale New Arrivals Heaviest Lightest')
    b = a[1].split('\n')
    if 'Previous' in b[2]:
        del b[:4]
    else:
        del b[:2]
    

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

    #print c

    # ing_list = [ 'name, amount, unit', 'price' ]
    
    ingredient_list = []

    for i in range(3): # put only 3 items in the list
        x=[]
        a = ing_list[2*i].split(',')
        b = len(a)
        amount = a[b-1]
        del a[b-1]
        name = ''
        for j in range(len(a)):
            name += a[j]
        x.append(name.lower()) # name
        b = amount.split(' ')
        
        x.append(b[1]) # amount
        x.append(b[2].lower()) # unit
        x.append(ing_list[2*i+1].lower()) # price
        x.append('iherb')
        ingredient_list.append(x)

    return ingredient_list





def walmart_search(ingredient):
    """
    input = str(ingredienet)
    output = [ [ingredient, amount, unit, price] * 3 ]
    """

    walmart_ingredient = ingredient.replace(" ","%20")
    walmart_url = 'http://www.walmart.com/search/?query='+walmart_ingredient    
    walmart = []

    walmart_html = urllib2.urlopen(walmart_url).read()
    walmart_text = plaintext(walmart_html)
    
    a = walmart_text.split('Sort Best match Best sellers Price: low to high Price: high to low Highest rating New')
    b = a[1].split('\n')
    
    
    #print b
    

    for i in range(len(b)):
        if b[i] == '':
            pass
        elif b[i][0] == '*':
            pass
        elif '/' in b[i] or 'rating' in b[i] or 'Rollback' in b[i] or 'Best Seller' in b[i]:
            pass
        elif b[i] == 'New':
            pass
        else:
            walmart.append(b[i])


    
    
    # walmart = [ 'name,amount,unit','price' ]

    ingredient_list = []

    for i in range(3):
        x = []
        a = walmart[2*i].split(',')
        x.append(a[0].lower()) # name 
        

        b = a[1].split(' ')

        x.append(b[1].lower()) # amount
        x.append(b[2].lower()) # unit
        x.append(walmart[2*i+1].lower()) # price
        x.append('walmart')
        ingredient_list.append(x)


    return ingredient_list
   

def produce_search(ingredient):
    """
    input = str(ingredienet)
    output = [ [ingredient, amount, unit, price]  ]
    """

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
            
    
    if len(ingredient_list) == 0:
        return ingredient_list
    else:
        for i in range(len(ingredient_list)):
            for j in range(len(ingredient_list)):
                if ingredient_list[i][3] <= ingredient_list[j][3]:
                    x = ingredient_list[i]
        
        return [x]






def unify_units(ingredient_list):
    """
    input = [ [ingredient, amount, unit, price] * 3 ]
    output = [ [ingredient, unified_amount, unified_unit, price] * 3 ]
    """

    unit = ['cup','tablespoon','teaspoon','pound','lb','g','gram']
    unify = [80, 0.5, 0.25, 16, 16, 0.035, 0.035]


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
                ingredient_list[i][1] = str(float(ingredient_list[i][1])*float(unify[j]))
                ingredient_list[i][2] = 'oz'
  
    return ingredient_list




def unify_recipe_unit(recipe_amount, recipe_unit):
    """
    recipe_amount = [amount1, amount2, amount3, ...]
    recipe_unit = [unit1, unit2, unit3, ...]
    output = [ [unified_amount1, unified_amount2,...],[unified_unit1, unified_unit2, ...] ]
    """

    unit = ['oz','ounce''cup','tablespoon','teaspoon','pound','lb']
    unify = [1, 1, 80, 0.5, 0.25, 16, 16, 0.03, 0.03]
    for i in range(len(recipe_unit)):
        for j in range(len(unit)):
            if unit[j] in recipe_unit[i]:
                recipe_amount[i] = recipe_amount[i] * unify[j]
                recipe_unit[i] = 'oz'

    return [recipe_amount, recipe_unit]




def compare_amount(ingredient_list, recipe_amount, recipe_unit):
    """
    ingredient_list = [ [ingredient, amount, unit, price] * 3 ]
    recipe_amount = string
    recipe_unit = string
    output = final one [[ingredient, amount, unit, price]]
    """
    
    a = [ingredient_list[0][3][1:],ingredient_list[1][3][1:],ingredient_list[2][3][1:]]
    
    a.sort()
    c = []
    for j in range(3):
        for i in range(3):
            if ingredient_list[i][3][1:]==a[j]:
                c.append(i)
    
    if recipe_unit == 'oz' and ingredient_list[c[0]][2] == 'oz':
        if recipe_amount < ingredient_list[c[0]][1] :
            return ingredient_list[c[0]]
        elif ingredient_list[c[1]][3] == 'n stores only':
            return ingredient_list[c[0]]
        elif recipe_amount < ingredient_list[c[1]][1] and ingredient_list[c[1]][1] < recipe_amount*2 :
            return ingredient_list[c[1]]
        elif ingredient_list[c[2]][3] == 'n stores only':
            return ingredient_list[c[1]]
        elif recipe_amount < ingredient_list[c[2]][1] and ingredient_list[c[2]][1] < recipe_amount*2 :
            return ingredient_list[c[2]]
        elif recipe_amount < ingredient_list[c[2]][1] and ingredient_list[c[2]][1] > recipe_amount*2 :
            return ingredient_list[c[1]]
        elif recipe_amount > ingredient_list[c[2]][1] :
            return ingredient_list[c[2]]
        else:
            ingredient_list[c[0]].append('mark')
            return ingredient_list[c[0]] # mark the number

    else:
        ingredient_list[c[0]].append('mark')
        return ingredient_list[c[0]] # mark the number
        



def ingredients_search(ingredient):
    """
    walmart = 3 lists
    iherb = 3 lists
    produce = 3 lists
    output = one of the results from walmart, iherb, produce
    """
    
    produce = produce_search(ingredient)

    if len(produce) != 0:
        return produce

    walmart = walmart_search(ingredient)
    

    walmart_prices = [walmart[0][3][1:],walmart[1][3][1:],walmart[2][3][1:]]
    walmart_prices.sort()
    
    

    if 'n stores only' not in walmart_prices:
        return walmart
    elif walmart_prices[2] == 'n stores only' and walmart_prices[1] != 'n stores only':
        return walmart


    iherb = iherb_search(ingredient)
    iherb_prices = [iherb[0][3][1:],iherb[1][3][1:],iherb[2][3][1:]]


    if min(walmart_prices[0],iherb_prices[0],iherb_prices[1],iherb_prices[2]) in walmart_prices :
        return walmart
    elif min(walmart_prices[0],iherb_prices[0],iherb_prices[1],iherb_prices[2]) in iherb_prices :
        return iherb




def refine_name(ingredient):
    """
    input = [ingredient1, ingredient2, ingredient3, ...]
    output = [refined_name1, refined_name2, refined_name3, ...]
    """
    for i in range(len(ingredient)):
        a = ingredient[i].find('or')
        if a != -1:
            ingredient[i] = ingredient[i][:a-1]

        b = ingredient[i].find('(')
        c = ingredient[i].find(')')
        if b != -1:
            ingredient[i] = ingredient[i][:a-1] + ingredient[i][b+1:]

        d = ingredient[i].find(',')
        if d != -1:
            ingredient[i] = ingredient[i][:d]
    return ingredient




def main(name_list, amount_list, unit_list):
    names = refine_name(name_list)
    amounts = unify_recipe_unit(amount_list, unit_list)[0]
    units = unify_recipe_unit(amount_list, unit_list)[1]

    final = []

    for i in range(len(names)):
        name = names[i]
        amount = amounts[i]
        unit = units[i]

        pre_item_list = ingredients_search(name)
        item_list = unify_units(pre_item_list)

        if len(item_list) == 1:
            item_list.append('catalog')
            final.append(item_list)
            
        if len(item_list) == 3:
            final_item = compare_amount(item_list,amount,unit)
            final_item.append
            final.append(final_item)
            

    return final

amount_list = [0.16666666666666666, 0.08333333333333333, 0.25, 0.16666666666666666, 0.3333333333333333, 0.3333333333333333, 0.08333333333333333, 0.16666666666666666, 0.3333333333333333]
unit_list = ['cup', 'cup', 'teaspoon', 'cup', 'teaspoon', 'cup', 'cup', 'cup', 'teaspoon']
name_list = ['white sugar ', 'margarine, melted ', 'ground nutmeg ', 'milk ', 'baking powder ', 'all-purpose flour ', 'margarine, melted ', 'white sugar ', 'ground cinnamon ']

#name_list = ['white sugar','black pepper','egg','bread']
#amount_list = [1,5,2,1]
#unit_list = ['cup','lb','oz','loaf']
print main(name_list, amount_list, unit_list)

#things to do => refine produce information / mark amount
