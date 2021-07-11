from flask import Flask, request, jsonify 
from connection import Connection 
import json

app = Flask(__name__)
conn = Connection('localhost', 5432, 'database_vendas', 'postgres', '12345')

clients = []

@app.route('/', methods=['GET'])
def get_product():
    return jsonify({ 'name': 'Valdir' })

# endpoints produtos
@app.errorhandler(400)
@app.route('/product/', methods=['GET'])
def get_products():
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            query = """SELECT * FROM produtos """
            cursor_pg.execute(query)
            results = cursor_pg.fetchall()

            all_products = []

            if not results:
                return jsonify({ 'erro':'Nenhum resultado encontrado' }), 400

            for x in results:                
                product = { "id" : x[0], "produto": x[1], "perc_comissao": x[2] }
                all_products.append(product)

        except Exception:
            return jsonify({ 'erro': 'Houve um erro interno' }), 401

    return jsonify(all_products)

@app.errorhandler(400)
@app.route('/product/save', methods=['GET','POST'])
def save_new_product():
    
    if request.method == 'POST':
        try:
            product = json.loads(request.data)

            if not product:
                return jsonify({ 'erro': 'produto nao cadastrado', 'code': '400' }), 400

            query = """ INSERT INTO produtos (produto, perc_comissao) VALUES ('{}','{}') 
            """.format(product['produto'], product['percentual'])

            cursor_pg = conn.cursor()
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()
                
            if rows_count > 0:
                return jsonify({ 'success': 'produto inserido com sucesso' }), 200    
          
        except Exception:  
            return jsonify({ 'status':'erro', 'mensagem': 'Não foi possível inserir o produto'})  
  
    return jsonify({ 'message': 'Endpoint para cadastrar produtos' })

# endpoints vendedor
@app.errorhandler(400)
@app.route('/seller', methods=['GET'])
def get_seller():
    if request.method == 'GET':
        # create cursor 
        cursor_pg = conn.cursor() 
        query = """SELECT * FROM vendedores """ 
        cursor_pg.execute(query)
        
        results = cursor_pg.fetchall()
        all_sellers = []

        if not results:
            return jsonify({ 'erro': 'Nenhum vendedor encontrado'}), 400

        for x in results:
            seller = { "id" : x[0], "nome": x[1] }
            all_sellers.append(seller)
        conn.close()    

    return jsonify(all_sellers)

@app.errorhandler(400)
@app.route("/seller/add", methods=['POST'])
def save_new_seller():
    if request.method == 'POST':
        seller = json.loads(request.data)

        try:
            if not seller:
                return jsonify({ 'erro': 'Vendedor não cadastrado', 'code': '400' }), 400
            seller_name = seller['nome']

            query = """ INSERT INTO vendedores (nome) VALUES ('{}') """.format( seller_name)
            # create cursor 
            cursor_pg = conn.cursor() 
            cursor_pg.execute(query)
            rows_count = cursor_pg.rowcount
            conn.commit()

            if rows_count > 0:
                return jsonify({ 'success': 'vendedor cadastrado com sucesso' })    

        except Exception:
            return jsonify({})

    return jsonify({'message': 'Endpoint para adicionar um vendedores'})


# endpoints cliente
@app.errorhandler(400)
@app.route('/client/', methods=['GET','POST'])
def insert_new_client():
    if request.method == 'POST':
        clientes = json.loads(request.data)
        pos = len(clientes)
        clientes['id'] = pos
        clients.append(clientes)

        if not clientes:
            return jsonify({ 'erro': 'produto nao cadastrado', 'code': '400' }), 400
        
        client_nome = clientes['nome']

        query = """ INSERT INTO cliente (nome) VALUES ('{}') """.format(client_nome)
        # create cursor 
        cursor_pg = conn.cursor() 
        cursor_pg.execute(query)
        rows_count = cursor_pg.rowcount
        conn.commit()

        if rows_count > 0:
            return jsonify({ 'success': 'cliente cadastrado com sucesso' }), 200
              
        return jsonify(clients[pos])
         
    elif request.method == 'GET':
        return jsonify(clients)

@app.route('/client/<int:id>', methods=['GET'])
def get_client(id):
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            query = """SELECT * FROM cliente WHERE id = {} """.format(id)
            cursor_pg.execute(query)

            data = cursor_pg.fetchone()
            response = { 
                 "id": data[0], 
                 "nome": data[1], 
                 "data_criacao": data[2] 
            }

        except Exception:

            message = "Cliente  não encontrado "
            response = { "status": "erro", "message": message, "code": 400 }

    return jsonify(response)
   

@app.route('/client/delete/<int:id>', methods=['GET','DELETE'])
def delete_cliente(id):
    if request.method == 'GET':
        try:
            cursor_pg = conn.cursor()
            query = """ DELETE FROM cliente WHERE id = {} """ .format(id)
            cursor_pg.execute(query)
            conn.commit()

            response = { 'success': "usuario excluido com sucesso" }

        except Exception:
            message = "Não foi possível excluir o cliente"
            response = { 'error': message }

        return jsonify(response)        
    

@app.route('/clients', methods=['GET'])
def get_all_clients():
    # create cursor 
    cursor_pg = conn.cursor() 
    query = """SELECT * FROM cliente """ 
    cursor_pg.execute(query)
    
    results = cursor_pg.fetchall()
    clients_data = []

    for x in results:
        client = { "id" : x[0], "nome": x[1], "data": x[2] }
        clients_data.append(client)
      
    conn.close()

    return jsonify(clients_data)     

if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.run(port=8888)