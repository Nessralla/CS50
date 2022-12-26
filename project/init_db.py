import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel,com) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Alexandre','09116629604','alexandre.nessralla@gmail.com','rua geralda rufino borges 280','veredas','araxa','MG','1231231231','34999232410','2')
            )

cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel,com) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
            ('Nilton','83692680319','qualquerum@gmail.com','alameda dos anjos','jardim zebu','araxa','MG','9137123123','34999447663','2')
            )

cur.execute("INSERT INTO leiloes (dia,lugar,leiloeiro,qtdLotes,encerrado,vlrMov,totalCom) VALUES (?,?,?,?,?,?,?)",
('2022-12-20','Estância Brasil', 'Rogério','0','SIM','0','0'))

cur.execute("INSERT INTO leiloes (dia,lugar,leiloeiro,qtdLotes,encerrado,vlrMov,totalCom) VALUES (?,?,?,?,?,?,?)",
('2022-12-27','Estância Brasil', 'Matheus','0','NAO','0','0'))

cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vlrVendido,comprador,vendedor,comissao) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('M','Nelore','36+','10','2','40000','42000','1','2','1600'))

cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vlrVendido,comprador,vendedor,comissao) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('F','Nelore','0-12','5','2','10000','9500','2','1','370'))

cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vlrVendido,comprador,vendedor,comissao) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('M','Nelore','12-24','8','2','20000','23000','1','2','920'))

cur.execute("INSERT INTO lotes (sexo,raca,idade,qtd,leilao,vlrPedido,vlrVendido,comprador,vendedor,comissao) VALUES (?,?,?,?,?,?,?,?,?,?)",
            ('M','Nelore','24-36','14','2','50000','49000','2','1','1000'))


connection.commit()
connection.close()