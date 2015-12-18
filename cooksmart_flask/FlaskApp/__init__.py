from flask import Flask, render_template, json, request, redirect, url_for
from flaskext.mysql import MySQL
import operator
from werkzeug import generate_password_hash, check_password_hash
from merge1 import *
from find_stores import *
import cache_from_db
import InsertDB 



USER_DICT = {"ingredients":["salt","eggs","scallions","onions","bread","ice cream"],
                  "history":["coffee","ice cream","sandwich","olin"]}
user_name = "Amon"

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cooksmart'
app.config['MYSQL_DATABASE_DB'] = 'cooksmart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/',methods=['POST','GET'])
def homepage():

    return render_template("main.html")


@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html", USER_DICT=USER_DICT, user_name = user_name)

@app.route('/register',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['username']
        _email = request.form['email']
        _password = request.form['password']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            # _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

@app.route("/Authenticate",methods=['POST','GET'])
def Authenticate():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from tbl_user where user_username='" + username + "' and user_password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return redirect(url_for('dashboard'))


@app.route('/search',methods=['POST','GET'])
def searchresult():
    searchquery = request.form['searchquery']
    f2fork = food2fork(searchquery)
    url = f2fork.getRecipeurl()
    for i in range(len(f2fork.f2furl_ingredients)):
        f2fork.getIngredients(i)
    try:
        final_ingre = f2fork.ingredients_lists[0]
        final_ingre = final_ingre[0]
        Parse = parse()
        recipe= Parse.recipe(url)
        dishname = Parse.dishname(url)
        servings = Parse.servings(url)
        SEARCH_DICT=[{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre,"servings":servings}]
        global sdict
        sdict=SEARCH_DICT
    except IndexError:
        return render_template("noresult.html")
    return render_template("searchresult.html", searchquery=searchquery, SEARCH_DICT = SEARCH_DICT, user_name = user_name)

@app.route('/computecost',methods=['POST','GET'])
def computecost():
    nofserving = request.form['nofserving']
    costcnvt=ready_for_cost()
    final_ingre=sdict[1]["ingre"]
    n_people=sdict[1]["servings"]
    m_people=int(nofserving)
    list_amount = costcnvt.amount(final_ingre,m_people,n_people)
    list_unit = costcnvt.unit(final_ingre)
    list_name = costcnvt.name(final_ingre)
    dishname = sdict[1]["dishname"]
    amount_list = [0.16666666666666666, 0.08333333333333333, 0.25, 0.16666666666666666, 0.3333333333333333, 0.3333333333333333, 0.08333333333333333, 0.16666666666666666, 0.3333333333333333]
    unit_list = ['cup', 'cup', 'teaspoon', 'cup', 'teaspoon', 'cup', 'cup', 'cup', 'teaspoon']
    name_list = ['coffee ', 'margarine, melted ', 'ground nutmeg ', 'milk ', 'baking powder ', 'all-purpose flour ', 'margarine, melted ', 'white sugar ', 'ground cinnamon ']
    cache_from_db.config(name_list,unit_list,amount_list)
    list_grocery = cache_from_db.find_cache_data()
    list_grocery.extend(InsertDB.searchnotindb(cache_from_db.names,cache_from_db.amounts,cache_from_db.units))


    findstore=find_stores()
    findstore.get_location('Olin way, Boston, MA')
    findstore.search_stores(1800)
    STORE_DICT = findstore.near_you()
    STORE_LIST = sorted(STORE_DICT.items(),key=operator.itemgetter(1))

    return render_template("computecost.html", dishname=dishname, nofserving=nofserving,list_grocery=list_grocery,user_name=user_name,STORE_LIST=STORE_LIST)


if __name__ == "__main__":
    app.run(debug=True)
