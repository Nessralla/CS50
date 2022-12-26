DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS leiloes;
DROP TABLE IF EXISTS lotes;


CREATE TABLE clients (
    clientId INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nome VARCHAR(45) NOT NULL,
    doc VARCHAR(15) NOT NULL,
    mail VARCHAR(30) NOT NULL,
    logradouro VARCHAR(45) NOT NULL,
    bairro VARCHAR(20) NOT NULL,
    cidade VARCHAR(20) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    inscRural VARCHAR(15) NOT NULL,
    tel VARCHAR(15) NOT NULL
);

CREATE TABLE leiloes (
    leilaoId INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dia DATE NOT NULL,
    lugar TEXT NOT NULL,
    leiloeiro TEXT NOT NULL,
    qtdLotes INTEGER DEFAULT 0,
    encerrado TEXT DEFAULT 'NAO',
    vlrMov TEXT DEFAULT 0,
    totalCom TEXT DEFAULT 0
);

CREATE TABLE lotes (
    lotesId INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sexo VARCHAR(1) NOT NULL,
    raca VARCHAR(10) NOT NULL,
    idade VARCHAR(10) NOT NULL,
    qtd INTEGER NOT NULL,
    leilao INTEGER,
    vlrPedido VARCHAR(20),
    vlrVendido VARCHAR(20),
    comprador INTEGER,
    vendedor INTEGER,
    comissao VARCHAR(10),
    FOREIGN KEY(leilao) REFERENCES leiloes(leilaoId),
    FOREIGN KEY(comprador) REFERENCES clients(clientId),
    FOREIGN KEY(vendedor) REFERENCES clients(clientId)    
);

