from flask import Flask, request, jsonify 
# from connection import Connection 
import json

import psycopg2 

app = Flask(__name__)

conn = psycopg2.connect(host='localhost', port=5432, database='dbaula_pqsl', user='postgres', password='12345')


@app.route('/', methods=['GET'])
def get_product():
    return jsonify({ 'name': 'Valdir' })


@app.route('/insert', methods=['GET','POST'])
def insert_new_product():
    return 'Pagina para inserir novo produto'


@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete_product_id(id):
    return 'Pagina para deletar produto'


@app.route('/sales', methods=['GET'])
def list_from_item():

    # create cursor 
    cursor_pg = conn.cursor()

    query = """SELECT * FROM usuario """ 
    cursor_pg.execute(query)

    query_results = cursor_pg.fetchall()

    person = []

    for x in query_results:
        person.append(x)
    
    cursor_pg.close()
    conn.close()

    return jsonify(person)

    
   
        

if __name__ == '__main__':
    
    app.run(port=8888)