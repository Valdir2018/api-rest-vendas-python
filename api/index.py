from flask import Flask, request, jsonify 
from connection import Connection 
import json

app = Flask(__name__)

conn = Connection('localhost', 5432, 'database_vendas', 'postgres', '12345')
# create cursor 
cursor_pg = conn.cursor()

clients = [
  
]

@app.route('/', methods=['GET'])
def get_product():
    return jsonify({ 'name': 'Valdir' })

@app.route('/client/', methods=['GET','POST'])
def insert_new_client():
    if request.method == 'POST':
        clientes = json.loads(request.data)
        pos = len(clientes)
        clientes['id'] = pos
        clients.append(clientes)

        client_nome = clientes['nome']

        query = """ INSERT INTO cliente (nome) 
        VALUES ('{}') """.format(client_nome)
        
        rows_count = cursor_pg.execute(query)
        conn.commit()

        if rows_count > 0:
            dados = { 'message': 'Cliente cadastrado com sucesso !' }
            return jsonify(dados)
        else:
            dados = { 'message': 'Não foi possivel cadastrar o cliente'}    

        return jsonify(clients[pos])
         
    elif request.method == 'GET':
        return jsonify(clients)




@app.route('/cliente/<int:id>', methods=['GET', 'POST'])
def get_client(id):

    if request.method == 'GET':

        try:
            response = clients[id]
        except IndexError:
          
            message = " Cliente  não encontrado "
            response = { "status": "erro", "mensagem": message }

        except Exception:
            message = " Houve um erro interno "
            response = { "status": "erro", "Mensagem": message } 
        return jsonify(response)
   


@app.route('/cliente/delete/<int:id>', methods=['GET','POST'])
def delete_cliente(id):
    
    return 'Pagina para deletar produto'

@app.route('/clientes', methods=['GET'])
def get_all_clients():

    query = """SELECT * FROM cliente """ 
    cursor_pg.execute(query)
    query_results = cursor_pg.fetchall()
    
    clients_data = []

    for x in query_results:
        cliente = { "id" : x[0], "nome": x[1], "data": x[2] }

        clients_data.append(cliente)
      
    cursor_pg.close()
    conn.close()

    return jsonify(clients_data)     

if __name__ == '__main__':
    
    app.run(port=8888)