from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_requireds
import sqlite3




app = Flask(__name__)

# Load database

connection = sqlite3.connect('database.db')

cur = connection.cursor()


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
@login_requireds
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    
    # esqueça o usuário
    session.clear()

    # se o usuário tiver tentado fazer login

    if request.method == 'POST':
        
        # ensure username was submitted
        if not request.form.get("username"):
            return render_template('error.html',msg='Must provide username')

            # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('error.html',msg='Must provide password')        

        # Query database for username
        rowsX = cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        print(rowsX)

        # Ensure username exists and password is correct
        if len(rowsX) != 1 or not check_password_hash(rowsX[0]["hash"], request.form.get("password")):
            print('deu errado')
            return render_template('error.html',msg='Invalid username or passqord')

        # Remember which user has logged in
        session["user_id"] = rowsX[0]["id"]

        # Redirect user to home page
        flash("You Sucessfuly login")
        return redirect("/")    


    else:

        return render_template("login.html")