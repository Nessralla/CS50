from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Load database

connection = sqlite3.connect('database.db')

cur = connection.cursor()



# CÓDIGO PARA INSERIR USUARIO ADMIN QUE POSSA FAZER LOGIN.

nome = input("Digite o nome do usuario: ")
senha = input("Digite a senha de admin:")

passHash = generate_password_hash(senha)

print(passHash)


# load admin into database

cur.execute("INSERT INTO users (username,hash) VALUES (?, ?)",
            (nome,passHash)
            )


connection.commit()
connection.close()


