from flask import Flask, request, jsonify 
from connection import Connection
import json

webapp = Flask(__name__)
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

    return jsonify(response)

@webapp.errorhandler(400)
@webapp.route('/client', methods=['POST'])
def insert_new_client():
    if request.method == 'POST':
        try:
            client = json.loads(request.data)
            if not client:
                return jsonify({ 'erro': 'cliente nao cadastrado' }), 400

            query = """ INSERT INTO clientes (nome) VALUES ('{}') 
            """.format(client['nome'])

            cursor_pg = conn.cursor()
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()
                    
            if rows_count > 0:
                return jsonify({ 'success': 'cliente cadastrado com sucesso' }), 201    
        except Exception:
            return jsonify({}), 201  

@webapp.errorhandler(400)
@webapp.route('/clients', methods=['GET'])
def get_all_clients():
    try:
        cursor_pg = conn.cursor() 
        cursor_pg.execute("""SELECT * FROM clientes """)
        
        results = cursor_pg.fetchall()
        clients_data = []

        for x in results:
            client = { "id" : x[0], "nome": x[1], "data": x[2] }
            clients_data.append(client)
        
        conn.close()

        return jsonify(clients_data), 200
    except Exception:
        return jsonify({'Erro':'Houve um erro interno'}), 400   

@webapp.errorhandler(400)
@webapp.route('/product', methods=['GET'])
def get_product():
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            cursor_pg.execute("""SELECT * FROM produtos """)
            results = cursor_pg.fetchall()

            all_products = []

            if not results:
                return jsonify({ 'erro':'Nenhum resultado encontrado' }), 400

            for x in results:                
                product = { "id" : x[0], "produto": x[1], "comissao": x[2] }
                all_products.append(product)

        except Exception:
            return jsonify({ 'erro': 'Houve um erro interno' })

    return jsonify(all_products), 200
    
@webapp.errorhandler(400)
@webapp.route('/product/add', methods=['POST'])
def save_new_product():
    if request.method == 'POST':
        try:
            product = json.loads(request.data)

            if not product:
                return jsonify({ 'erro': 'produto nao cadastrado' }), 400

            query = """ INSERT INTO produtos (produto, perc_comissao) VALUES ('{}','{}') 
            """.format(product['produto'], product['percentual'])

            cursor_pg = conn.cursor()
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()
                
            if rows_count > 0:
                return jsonify({ 'success': 'produto inserido com sucesso' }), 201    
          
        except Exception:  
            return jsonify({ 'status':'erro', 'mensagem': 'Não foi possível inserir o produto'})  
  
    return jsonify(product)

@webapp.errorhandler(400)
@webapp.route('/seller/<int:id>', methods=['GET'])
def get_one_seller(id):
    if request.method == 'GET':
       try:
            cursor_pg = conn.cursor()
            cursor_pg.execute("""SELECT * FROM vendedores WHERE id = {} """.format(id))
            conn.commit()
            
            results = cursor_pg.fetchall()
            all_sellers = []

            if not results:
                return jsonify({ 'erro': 'Nenhum vendedor encontrado'}), 400

            for x in results:
                seller = { "id" : x[0], "nome": x[1] }
                all_sellers.append(seller)
            conn.close()
       except Exception:
           return jsonify({})    
    
    return jsonify(results), 200
   

@webapp.errorhandler(400)
@webapp.route('/seller/add', methods=['POST'])
def save_new_seller():
    if request.method == 'POST':
        seller = json.loads(request.data)
        try:
            if not seller:
                return jsonify({ 'erro': 'Vendedor não cadastrado', 'code': '400' }), 400
            seller_name = seller['nome']

            query = """ INSERT INTO vendedores (nome) VALUES ('{}') """.format( seller_name)
            cursor_pg = conn.cursor() 
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()

            if rows_count > 0:
                return jsonify({ 'success': 'vendedor cadastrado com sucesso' })    

        except Exception:
            return jsonify({})

    return jsonify(seller), 201
    

if __name__ == '__main__':
    webapp.config["DEBUG"] = True
    webapp.run(port=8888)
