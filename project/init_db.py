import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nome,doc,mail,logradouro,bairro,cidade,estado,inscRural,tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Alexandre','09116629604','alexandre.nessralla@gmail.com','rua geralda rufino borges 280','veredas','araxa','MG','1231231231','34999232410')
            )


connection.commit()
connection.close()