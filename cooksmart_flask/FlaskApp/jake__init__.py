from flask import Flask, render_template, json, flash, request, url_for, redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kaist0826'
app.config['MYSQL_DATABASE_DB'] = 'cooksmart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/',methods=['POST','GET'])
def homepage():

    return render_template("main.html")



@app.route('/dashboard/')
def dashboard():
    return render_template("example.html")

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

@app.route('/login', methods=['POST','GET'])
def login():
    
    error = ''
    try:
    
        if request.method == "POST":
            attempted_email = request.form['email']
            attempted_password = request.form['password']
            #flash(attempted_username)
            #flash(attempted_password)
            if attempted_email == "yuntae1000@gmail.com" and attempted_password == "123":
                return redirect(url_for('dashboard'))                
            else:
                error = "Invalid credentials. Try Again."
        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)  


if __name__ == "__main__":
    app.run(debug=True)
