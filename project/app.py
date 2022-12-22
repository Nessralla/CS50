from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_requireds
import sqlite3




app = Flask(__name__)

# Load database

connection = sqlite3.connect('database.db',check_same_thread=False)

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
        rowsX = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        # print(rowsX.arraysize)
        user = rowsX.fetchall()
        senhaHash = user[0][2]
        # print(senhaHash)

        # Ensure username exists and password is correct
        if (rowsX.arraysize != 1) or not check_password_hash(senhaHash, request.form.get("password")):
            print('deu errado')
            return render_template('error.html',msg='Invalid username or passqord')

        # Remember which user has logged in
        user_id = user[0][0]
        session["user_id"] = user_id

        # Redirect user to home page
        flash("You Sucessfuly login")
        return redirect("/")    


    else:

        return render_template("login.html")

@app.route('/clientes')
@login_requireds
def clients():

    # Query database for clients
    rows = cur.execute("SELECT * FROM clients")

    clients = rows.fetchall()
    # print(clients) 

    return render_template('clientes.html',clients=clients)


@app.route('/cadastro')
@login_requireds
def cadastrar():

    # check method
    if request.method == 'POST':
        return render_template('error.html',msg='Ainda por fazer')
    else:
        return render_template('cadastro.html')


@app.route('/leiloes')
@login_requireds
def leiloes():
    
    # Query database for clients
    rows = cur.execute("SELECT * FROM leiloes")

    leiloes = rows.fetchall()
    # print(clients)
    #  
    return render_template('leiloes.html',leiloes=leiloes)

@app.route('/lotes')
@login_requireds
def lotes():
    return render_template('lotes.html')