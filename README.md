# api-rest-vendas-python
Api de vendas  com python e flask

O arquivo database.sql contém o script do banco de dados postgres

O requirements-dev.txt, na raíz do projeto contém a lista dos pacotes utilizados para criar a api e efetuar os testes. 

As credenciais de acesso ao banco de dados deverão ser inseridas no arquivo principal app.py


Retornar todos os clientes: http://localhost:8888/app/clients/

Retornar  um cliente: http://localhost:8888/app/client/1

Adicionar um novo cliente: http://localhost:8888/app/client/add

Retornar  um produto pelo nome: http://localhost:8888/app/product/Celular

Adicionar um novo produto: http://localhost:8888/app/product/add

Retornar  um determinado vendedor pelo id: http://localhost:8888/app/seller/1

Retornar a comissao de um determinado vendedor pelo nome: http://localhost:8888/app/seller/nome_vendedor

Retorna lista de todos os vendedores: http://localhost:8888/app/seller/

Adicionar um  novo vendedor: http://localhost:8888/app/seller/add

Adicionar uma  nova venda: http://localhost:8888/app/seller/add



