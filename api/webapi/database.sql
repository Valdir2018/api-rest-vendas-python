
CREATE DATABASE database_vendas;
USE database_vendas;


CREATE TABLE produtos(
   id SERIAL NOT NULL PRIMARY KEY,
   produto VARCHAR(120) NOT NULL,
   perc_comissao VARCHAR(12) NOT NULL,
   created_date DATETIME
)


CREATE TABLE  vendedor (
    id SERIAL NOT NULL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
)


CREATE TABLE clientes(
   id SERIAL PRIMARY KEY
   nome VARCHAR(120) NOT NULL,
   created DATE NOT NULL DEFAULT CURRENT_DATE

)

CREATE TABLE vendas (
 id SERIAL NOT NULL PRIMARY KEY,
 vendedor VARCHAR(100) NOT NULL,
 cliente VARCHAR(100) NOT NULL,
 total_vendas VARCHAR(12) NOT NULL,
 quantidade SMALLINT NOT NULL,
 comissao VARCHAR(10) NOT NULL,	
 hora_venda TIME
)

