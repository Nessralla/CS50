import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Alexandre','09116629604','alexandre.nessralla@gmail.com','rua geralda rufino borges 280','veredas','araxa','MG','1231231231','34999232410')
            )

cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Nilton','83692680319','qualquerum@gmail.com','alameda dos anjos','jardim zebu','araxa','MG','9137123123','34999447663')
            )

cur.execute("INSERT INTO leiloes (dia,lugar,leiloeiro,qtdLotes,encerrado,vlrMov,totalCom) VALUES (?,?,?,?,?,?,?)",
('2022-12-20','Estância Brasil', 'Rogério','0','FALSE','0','0'))

cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vlrVendido,comprador,vendedor,comissao) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('M','Nelore','36+','10','1','10000','8900','1','1','500'))


connection.commit()
connection.close()