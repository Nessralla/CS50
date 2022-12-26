Projeto Final CS 50

- Aplicação Web de gerenciamento de leilão de gado / Web application for Livestock Cattle Auction

Descrição/Description:
 Esta aplicação Web foi feita para completar o curso CS50 de Harvard. É uma aplicação que gerencia lotes e clientes de um determinado leilão, no caso de gado. Através da aplicação o usuário poderá cadastrar clientes, lotes e leilões, obtendo assim informações de inteligência de negócio, com dashboards e dados importantes. Feita no VSCode com flask e  sqlite3.
 Versão de uso privado e com potencial de negócio.

 This web application was coded for the final project of CS50x Harvard. Its an apliccation that manages drafets, clients from a determined auction house, in this example, livestock cattle. This apliccation allows the user to create drafts, clients and auctions, obtaining importante informations and reports from dashboards. Made in VSCode with flask, sqlite3 and bootstrap. 
 Version of private use and businnes usage.



Para rodar / To run:

No diretório do projeto, digite no powershell para rodar o app
    - set FLASK_APP="app.py"
    - $env:FLASK_APP = "app.py"
    - flask run
    

Web Application Pages
    - cadastro.html  : Insert clients into database
    - cadLeilao.html : Insert auctions into db
    - cadLotes.html  : Insert drafts into db
    - clients.html   : View all clients form db
    - error.html     : Standard page for errors
    - index.html     : View dashboads
    - layout.html    : layout for web page
    - leiloes.html   : View all auctions
    - login.html     : Login user
    - lotes.html     : view all drafts


Database (from schema.sql)
    - table clientes
    - table users
    - table leiloes
    - table lotes


Version 0:
    - MVP

Version 1:
    - Verify data inserted via HTML form in all routes
    - Improve security
    - Details from clients and more important information
    - Make online deploy