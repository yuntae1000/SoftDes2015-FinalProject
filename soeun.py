import urllib2
import sys
from pattern.web import *
reload(sys)
sys.setdefaultencoding('utf8')

def allrecipes(url):
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


def closetcooking(url):
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
    




#url = 'http://allrecipes.com/recipe/24263/ground-beef-enchiladas/?internalSource=previously%20viewed&referringContentType=home%20page'
#print allrecipes(url)

#url = 'http://www.closetcooking.com/2012/01/bacon-double-cheese-burger-dip.html'
#print closetcooking(url)

