from flask import Flask, request, jsonify 
from connection import Connection
from flask_cors import CORS
import json

webapp = Flask(__name__)
CORS(webapp)

conn = Connection('localhost', 5432, 'database_vendas', 'postgres', '12345')

@webapp.route('/')
def init():
    return 'My WebApp', 200

@webapp.errorhandler(400)
@webapp.route('/client/<int:id>', methods=['GET'])
def get_client(id):
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            query = """SELECT * FROM clientes WHERE id = {} """.format(id)
            cursor_pg.execute(query)

            data = cursor_pg.fetchone()
            response = {  "id": data[0], "nome": data[1], "data_criacao": data[2] }

        except Exception:
            message = "Cliente  não encontrado "
            response = { "status": "erro", "message": message }, 400

    return jsonify(response), 200

@webapp.errorhandler(400)
@webapp.route('/client/add', methods=['POST'])
def insert_new_client():
    if request.method == 'POST':
        try:
            client = json.loads(request.data)
            if not client:
                return jsonify({ 'erro': 'cliente nao cadastrado' }), 400

            cursor_pg = conn.cursor()
            query = """ INSERT INTO clientes (nome) VALUES ('{}') """.format(client['nome'])

            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()
                    
            if rows_count > 0:
                return jsonify({ 'success': 'cliente cadastrado com sucesso' }), 201    
        except Exception:
            return jsonify({}), 201  

@webapp.errorhandler(400)
@webapp.route('/clients/', methods=['GET'])
def get_all_clients():
    try:
        cursor_pg = conn.cursor() 
        cursor_pg.execute("""SELECT * FROM clientes """)
        results = cursor_pg.fetchall()
        clients_data = []

        for x in results:
            clients_data.append( { "id" : x[0], "nome": x[1], "data": x[2] })
        
        return jsonify(clients_data), 200
    except Exception:
        return jsonify({'Erro':'Houve um erro interno'}), 400   

@webapp.errorhandler(400)
@webapp.route('/product/<string:name>', methods=['GET'])
def get_product(name):
    if request.method == 'GET':
        
        try:
            cursor_pg = conn.cursor()
            query = """SELECT * FROM produtos WHERE produto LIKE '%{prod}%' """.format(prod=name)

            cursor_pg.execute(query)
            results = cursor_pg.fetchall()
            all_products = []

            for x in results:                
                all_products.append( { "id" : x[0], "produto": x[1], "preco": x[2], "comissao": x[3] })

            return jsonify(all_products), 200    

        except Exception:
            return jsonify({ 'erro':'Nenhum resultado encontrado' }), 400

    
@webapp.errorhandler(400)
@webapp.route('/product/add', methods=['GET','POST'])
def save_new_product():
    if request.method == 'POST':
        try:
            product = json.loads(request.data)

            if not product:
                return jsonify({ 'erro': 'produto nao cadastrado' }), 400

            query = """ INSERT INTO produtos (produto, preco, perc_comissao) VALUES ('{}','{}','{}') 
            """.format(product['produto'], product['preco'],  product['percentual'])

            cursor_pg = conn.cursor()
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()
           
                
            if rows_count > 0:
                return jsonify({ 'success': 'produto inserido com sucesso'}), 201    
          
        except Exception:  
            return jsonify({ 'status':'erro', 'mensagem': 'Não foi possível inserir o produto'})  
  

@webapp.errorhandler(400)
@webapp.route('/seller/<int:id>', methods=['GET'])
def get_one_seller(id):
    if request.method == 'GET':
       try:
            cursor_pg = conn.cursor()
            query = """SELECT * FROM vendedores WHERE id = {} """.format(id)
            cursor_pg.execute(query)
            conn.commit()
            
            results = cursor_pg.fetchall()
            all_sellers = []

            if not results:
                return jsonify({ 'erro': 'Nenhum vendedor encontrado'}), 400

            for x in results:
                all_sellers.append({ "id" : x[0], "nome": x[1] })
            return jsonify(all_sellers), 200

       except Exception:
           return jsonify({})    
    

@webapp.errorhandler(400)
@webapp.route('/seller/', methods=['GET'])
def get_all_seller():
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            cursor_pg.execute("""SELECT * FROM vendedores """)
            conn.commit()
            all_sellers = []
                
            results = cursor_pg.fetchall()
           
            for res in results:
                all_sellers.append( { "id" : res[0], "nome": res[1] })
            return jsonify(all_sellers), 200  

        except Exception:
            return jsonify({ 'erro': 'Nenhum vendedor encontrado'})      


@webapp.errorhandler(400)
@webapp.route('/seller/add', methods=['GET','POST'])
def save_new_seller():
    if request.method == 'POST':
        seller = json.loads(request.data)
        try:
            if not seller:
                return jsonify({ 'erro': 'Vendedor não cadastrado' }), 400

            query = """ INSERT INTO vendedores (nome) VALUES ('{}') """.format(seller['nome'])
            cursor_pg = conn.cursor() 
            cursor_pg.execute(query)
            conn.commit()
            rows_count = cursor_pg.rowcount
          

            if rows_count > 0:
                return jsonify({ 'success': 'vendedor cadastrado com sucesso' }), 201
                    
        except Exception:
            return jsonify({})


if __name__ == '__main__':
    webapp.config["DEBUG"] = True
    webapp.run(port=8888)
