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

# LOGIN E LOGOUT

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
        flash("You Sucessfuly login",'alert-primary')
        return redirect("/")    


    else:

        return render_template("login.html")


# EXIBIÇÃO DE CLIENTES, CADASTRO, DETALHES E ALTERAÇÕES

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

        flash("Cliente Cadastrado com Sucesso",'alert-primary')

        return render_template('cadastro.html')
    else:
        return render_template('cadastro.html')


@app.route('/clientDetail',methods=['POST'])
@login_requireds
def clientDetail():

    idCliente = request.form.get('detalheClient')

    row = cur.execute("SELECT * FROM clients WHERE clientId = ?",idCliente)
    cliente = row.fetchall()[0]
    # print(cliente[0][0])

    compradosObj = cur.execute("SELECT SUM(vlrVendido),COUNT(vlrVendido) FROM lotes WHERE comprador = ?",(cliente[0],))
    # print(compradosObj.fetchall())
    comprados = compradosObj.fetchall()

    vendidosObj = cur.execute("SELECT SUM(vlrVendido),COUNT(vlrVendido) FROM lotes WHERE vendedor = ?",(cliente[0],))
    # print(vendidosObj.fetchall())
    vendidos = vendidosObj.fetchall()


    #print(comprados,vendidos)



    return render_template('clientDetail.html',cliente=cliente,comprados=comprados,vendidos=vendidos)


# EXIBIÇÃO DE LEILAO, CADASTRO, DETALHES E ALTERAÇÕES


@app.route('/leiloes')
@login_requireds
def leiloes():
    
    # Query database for leiloes
    rows = cur.execute("SELECT * FROM leiloes")

    leiloes = rows.fetchall()

    # update qtdLotes, vlrMov e totalCom na tabela leiloes com as informações dos lotes dos leilões não encerrados
    objeto = cur.execute("SELECT leilaoId FROM leiloes WHERE encerrado = 'NAO'")
    leiloesAtivos = objeto.fetchall()

    for leilaoAtivo in leiloesAtivos:
        # Cada leilaoAtivo é uma tupla
        # print(leilaoAtivo)

        # Retornar a soma dos lotes, do total negociado e das comissoes para armazenar na base
        totalLotes = (cur.execute("SELECT COUNT(lotesId) FROM lotes WHERE leilao = ?",leilaoAtivo)).fetchall()
        totalNegociado = (cur.execute("SELECT SUM(vlrVendido) FROM lotes WHERE leilao = ?",leilaoAtivo)).fetchall()
        totalComissoes = (cur.execute("SELECT SUM(comissao) FROM lotes WHERE leilao = ?",leilaoAtivo)).fetchall()

        # print(totalComissoes[0][0],totalLotes[0][0],totalNegociado[0][0])

        # inserir na base dos leiloes os valores obtidos
        cur.execute("UPDATE leiloes SET qtdLotes = ?, vlrMov = ?,totalCom = ? WHERE leilaoId = ? ",(totalLotes[0][0],totalNegociado[0][0],totalComissoes[0][0],leilaoAtivo[0]))

        connection.commit()
      
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
        if not data:
            flash('Campo data deve ser preenchido','alert-danger')
            return render_template('cadLeilao.html')

        if not leiloeiro:
            flash('Campo Leiloeiro deve ser preenchido','alert-danger')
            return render_template('cadLeilao.html')

        if not local:
            flash('Campo local deve ser preenchido','alert-danger')
            return render_template('cadLeilao.html')


        # Insert Data 
        cur.execute("INSERT INTO leiloes (dia,lugar,leiloeiro) VALUES (?,?,?)",
        (data,local,leiloeiro))

        connection.commit()

        flash("Leilão Cadastrado com Sucesso",'alert-primary')

        return render_template('cadLeilao.html')
    else:
        return render_template('cadLeilao.html')


@app.route('/leilaoDetail',methods=["POST"])
@login_requireds
def leilaoDetail():

    # id do leilao selecionado
    idLeilao = request.form.get('detalheLeilao')
    # print(idLeilao)
    
    # retornar dict com clientes

    # Query DB for clients
    clientsObj = (cur.execute("SELECT clientId,nome FROM clients"))
    clientsList = clientsObj.fetchall()
    # print(clients)
    clients = dict()
    for client in clientsList:
        # print(client)       
        k = client[0]
        v = client[1]
        clients[k] = v
    #print(clients)

    # retornar info de todos os lotes do leilao

    rows = cur.execute("SELECT * from lotes WHERE leilao = ?",(idLeilao,))
    lotesDoLeilao = rows.fetchall()
    # print(lotesDoLeilao)


    # soma dos valores vendidos, soma das comissões, total de lotes
    totalNegociado = 0
    totalComissoes = 0
    totalLotes = len(lotesDoLeilao)

    for lote in lotesDoLeilao:
        totalComissoes += int(lote[11])
        totalNegociado += int(lote[8])

    infos = totalNegociado,totalComissoes,totalLotes
    
    return render_template('leilaoDetail.html',lotesDoLeilao=lotesDoLeilao,clients=clients,infos=infos)



# EXIBIÇÃO DE LOTES, CADASTRO, DETALHES E ALTERAÇÕES


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
        idLeilao = request.form.get('leilao')
        sexo = request.form.get('sexo')
        raca = request.form.get('raca')
        idade = request.form.get('idade')
        qtd = request.form.get('qtd')
        vlrPedido = request.form.get('valorPedido')
        vendedor = request.form.get('vendedor')
        # print(idLeilao,sexo,raca,idade,qtd,vlrPedido,vendedor)

        # Verify info

        # insert data
        cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vendedor) VALUES (?,?,?,?,?,?,?)",
            (sexo,raca,idade,qtd,idLeilao,vlrPedido,vendedor))

        connection.commit()

        flash("Lote Cadastrado com Sucesso",'alert-primary')

        return render_template('cadLotes.html')
    else:
        # Query database for lotes
        rows = cur.execute("SELECT leilaoId,dia FROM leiloes WHERE encerrado = 'NAO'")
        leiloes = rows.fetchall()
        # print(leiloes)

        # Query DB for clients
        clientsObj = (cur.execute("SELECT clientId,nome FROM clients"))
        clientsList = clientsObj.fetchall()
        # print(clientsList)

        return render_template('cadLotes.html',leiloes=leiloes,clientsList=clientsList)



@app.route('/loteDetail', methods=["POST"])
@login_requireds
def loteDetail():

    # id from detail lote
    lote = request.form.get('detalheLote')
    # print(lote)

    # Query database for lote selecionado
    rows = cur.execute("SELECT * FROM lotes WHERE lotesId = ?",lote)

    loteInfo = (rows.fetchall())[0]
    # print(loteInfo) 

    idLeilao = loteInfo[0]
    compradorId = loteInfo[-3]
    vendedorId = loteInfo[-2]

    # print(idLeilao,compradorId,vendedorId)

    # query db for data leilao
    dataLeilao = (cur.execute("SELECT dia FROM leiloes WHERE leilaoId = ?",(idLeilao,))).fetchall()
    # print(dataLeilao)

    # query db for comprador e vendedor
    comprador = (cur.execute("SELECT nome FROM clients WHERE clientId = ?",(compradorId,))).fetchall()
    vendedor = (cur.execute("SELECT nome FROM clients WHERE clientId = ?",(vendedorId,))).fetchall()

    # print(comprador,vendedor)
    

    return render_template('loteDetail.html',loteInfo=loteInfo,dataLeilao=dataLeilao, comprador=comprador,vendedor=vendedor)


@app.route('/relatorios',methods = ['GET','POST'])
@login_requireds
def relatorios():

    # check method
    if request.method == 'POST':




        return render_template('resultado.html')

    # return all id from clients
    clientObj = cur.execute("SELECT clientId FROM clients")
    clientesId = clientObj.fetchall(0)

    # return all lotesId from lotes
    lotesObj = cur.execute("SELECT lotesId FROM lotes")
    lotesId = lotesObj.fetchall(0)

    # return all leiloesId from leiloes
    leilaoObj = cur.execute("SELECT leilaoId FROM leiloes")
    leiloesId = leilaoObj.fetchall()

    print(clientesId,lotesId,leiloesId)

    return render_template('relatorios.html',clientesId=clientesId,lotesId=lotesId,leiloesId=leiloesId)