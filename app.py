from flask import Flask
from flask import render_template
from flask import request
from flask import session, redirect
from flask_session import Session


import sqlite3

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginuser", methods = ['POST', 'GET'])
def loginuser():
    if request.method == 'POST':
        username = request.form['t1']
        pwd = request.form['t2']
        with sqlite3.connect('database.db') as conn:
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            user = cur.execute("SELECT * FROM USER where UserName = ?",(username,)).fetchone()
            print(user)

            errors = []           
            if user == None:
               errors.append("user does not exists")
               return render_template("login.html", errors = errors)
            if(user['userpwd'] == pwd):
                session['username'] = username
                return  render_template('home.html')
            else:
                errors.append("username and password does not match")
                return render_template('login.html', errors = errors)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/chart")
def chart():
    return render_template("chart.html")       



@app.route("/aboutus")
def aboutus():
    return render_template("About2US.html")

@app.route("/menu")
def menu():
    return render_template("dummy.html")

@app.route("/registeruser")
def register():
    return render_template("register.html")

@app.route("/adduser", methods = ['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        try:
            uname = request.form['formuser']
            uemail = request.form['formemail']
            upwd = request.form['formpwd']
            umobile = request.form['formmobile']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO USER (UserName, email, userpwd, mobileNumber) VALUES (?,?,?,?)", (uname, uemail, upwd, umobile))

                conn.commit()
                message = "User created successfully"
                message = "welcome " + uname
        except:
            conn.rollback()
            message = "Error has occured"
        finally:
            conn.close()
            return render_template('login.html', msg = message)
        
@app.route("/profile")
def profile():
    
    username = session['username']
    with sqlite3.connect('database.db') as conn:
       cur = conn.cursor()
       uname = cur.execute("SELECT * FROM USER where UserName = ?",(username,)).fetchone()
       print(uname[1])
    return render_template("profile.html", data = uname)

@app.route("/updateuser")
def updateuser():
    username = session['username']
    with sqlite3.connect('database.db') as conn:
       cur = conn.cursor()
       uname = cur.execute("SELECT * FROM USER where UserName = ?",(username,)).fetchone()
    return render_template("update.html", data = uname)

@app.route("/updateuserrec", methods = ['POST', 'GET'])
def updateuserrec():
    if request.method == 'POST':
        uname = request.form['formuser']
        uemail = request.form['formemail']
        upwd = request.form['formpwd']
        umobile = request.form['formmobile']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("UPDATE USER SET userpwd = ?, mobileNumber = ?, email= ? WHERE UserName = ?",(upwd, umobile,uemail,uname))
            conn.commit()
    return render_template("home.html")

@app.route("/deleteuser", methods = ['POST', 'GET'])
def deleteuser():
    username = session['username']
    with sqlite3.connect('database.db') as conn:
       cur = conn.cursor()
       cur.execute("DELETE FROM USER WHERE UserName = ?",(username,))
       conn.commit()
    return redirect("/")