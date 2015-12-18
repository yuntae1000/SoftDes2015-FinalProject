from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import operator
from werkzeug import generate_password_hash, check_password_hash
from merge1 import *
from find_stores import *
from soeun import main



USER_DICT = {"Basics":[["Introduction to Python","/introduction-to-python-programming/"],
                            ["Print functions and Strings","/python-tutorial-print-function-strings/"],
                            ["Math basics with Python 3","/math-basics-python-3-beginner-tutorial/"]],
                  "Web Dev":[]}
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
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
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
    username = request.form('username')
    password = request.form('password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from tbl_user where username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return render_template("example.html")


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
        SEARCH_DICT=[{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre},{"dishname":dishname,"url":url,"recipe":recipe,"ingre":final_ingre}]
        global sdict
        sdict=SEARCH_DICT
    except IndexError:
        return render_template("noresult.html")
    return render_template("searchresult.html", searchquery=searchquery, SEARCH_DICT = SEARCH_DICT, user_name = user_name)

@app.route('/computecost',methods=['POST','GET'])
def computecost():
    nofserving = request.form['nofserving']
    selectedresult = request.form['selectedresult']
    findstore=find_stores()
    findstore.get_location('Olin way, Boston, MA')
    findstore.search_stores(1800)
    STORE_DICT = findstore.near_you()
    STORE_LIST = sorted(STORE_DICT.items(),key=operator.itemgetter(1))


    costcnvt=ready_for_cost()
    final_ingre=sdict[selectedresult]["ingre"]
    list_amount = costcnvt.amount(final_ingre)
    list_unit = costcnvt.unit(final_ingre)
    list_name = costcnvt.name(final_ingre)



    return render_template("computecost.html", USER_DICT=USER_DICT,nofserving=nofserving,selectedresult=selectedresult,STORE_LIST=STORE_LIST)

@app.route('/computecost2/',methods=['POST','GET'])
def computecost2():
    nofserving=1
    selectedresult="aaa"
    return render_template("computecost.html", USER_DICT=USER_DICT,nofserving=nofserving,selectedresult=selectedresult)


if __name__ == "__main__":
    app.run(debug=True)