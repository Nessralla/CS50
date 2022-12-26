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


@app.route('/cadastro', methods=["GET", "POST"])
@login_requireds
def cadastrar():

    # check method
    if request.method == 'POST':
        nome = request.form.get('clientName')
        doc = request.form.get('cpfCNPJ')
        mail = request.form.get('mail')
        ende = request.form.get('endereco')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        tel = request.form.get('telefone')
        insc = request.form.get('inscRural')
        # print(nome,doc,mail,ende,bairro,cidade,estado,tel,insc)

       # Verify info

       # Insert Data 
        cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (nome,doc,mail,ende,bairro,cidade,estado,tel,insc)
            )

        connection.commit()

        flash("Cliente Cadastrado com Sucesso")

        return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')


@app.route('/leiloes')
@login_requireds
def leiloes():
    
    # Query database for clients
    rows = cur.execute("SELECT * FROM leiloes")

    leiloes = rows.fetchall()
    # print(clients)
      
    return render_template('leiloes.html',leiloes=leiloes)


@app.route('/cadLeilao', methods=["GET", "POST"])
@login_requireds
def cadLeilao():

    # check method
    if request.method == 'POST':
        data = request.form.get('dataLeilao')
        leiloeiro = request.form.get('leiloeiro')
        local = request.form.get('local')

        # Verify data

        # Insert Data 
        cur.execute("INSERT INTO leiloes (dia,lugar,leiloeiro) VALUES (?,?,?)",
        (data,local,leiloeiro))

        connection.commit()

        flash("Leilão Cadastrado com Sucesso")

        return render_template('cadLeilao.html')
    else:
        return render_template('cadLeilao.html')

@app.route('/lotes')
@login_requireds
def lotes():

    # Query database for lotes
    rows = cur.execute("SELECT * FROM lotes")
    lotes = rows.fetchall()

    # Query DB for clients
    clientsObj = (cur.execute("SELECT clientId,nome FROM clients"))
    clientsList = clientsObj.fetchall()
    # print(clients)
    clients = dict()
    for client in clientsList:
        # print(client)       
        k = client[0]
        v = client[1]
        # print(k,v)
        clients[k] = v
        # print(clients)
    return render_template('lotes.html',lotes=lotes,clients=clients)

@app.route('/cadLotes', methods=["GET", "POST"])
@login_requireds
def cadLotes():

    # check method
    if request.method == 'POST':

        return render_template('error.html',msg='Ainda por fazer')
    else:
        # Query database for lotes
        rows = cur.execute("SELECT dia FROM leiloes WHERE encerrado = 'NAO'")
        # print(rows.fetchall())
        lotes = rows.fetchall()

        # Query DB for clients
        clientsObj = (cur.execute("SELECT clientId,nome FROM clients"))
        clientsList = clientsObj.fetchall()
        # print(clients)

        # transform Data into dict
        clients = dict()
        for client in clientsList:
            # print(client)       
            k = client[0]
            v = client[1]
            # print(k,v)
            clients[k] = v
            # print(clients)
        return render_template('cadLotes.html')