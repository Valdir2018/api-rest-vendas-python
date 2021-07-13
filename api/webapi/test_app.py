from unittest import mock, TestCase
from app import webapp
import json


class TestApp(TestCase):
    def setUp(self):
      self.client = webapp.test_client()

    def test_init_return_code_200(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)  

    def test_get_client_from_id_return_code_200(self):
        # o codigo de status deve ser 200
        response = self.client.get('/client/3')
        self.assertEqual(200, response.status_code)

    def test_get_client_from_id_return_json(self):
        # quando acessar /client/1 é esperado um objeto json
        response = self.client.get('/client/3')
        self.assertEqual('application/json', response.content_type)    

    # @mock.patch('app.create_new_client_db')
    def test_insert_new_client_return_code_201(self):
        client = { 'nome': 'Valdir' }
        response = self.client.post('/client', json=client)
        self.assertEqual(201, response.status_code)

    # @mock.patch('app.create_new_client_db')
    def test_insert_new_client_return_json(self):
        client = { 'nome': 'Jose' }
        response = self.client.post('/client', json=client)
        self.assertEqual('application/json', response.content_type)

    def test_get_all_clients_return_code_200(self):
        response = self.client.get('/clients')
        self.assertEqual(200, response.status_code)

    def test_get_all_clients_return_json(self):
        response = self.client.get('/clients')
        self.assertEqual('application/json', response.content_type) 

    def test_get_products_return_code_200(self):
        response = self.client.get('/product')
        self.assertEqual(200, response.status_code) 

    def test_get_products_return_json(self):
        response = self.client.get('/product')
        self.assertEqual('application/json', response.content_type)

    def test_save_new_product_return_code_200(self):
        product = { 'nome':'celular'}
        response = self.client.post('/product/add', json=product)
        self.assertEqual(201, response.status_code)

    def test_save_new_product_return_code_200(self):
        product = { 'nome':'celular'}
        response = self.client.post('/product/add', json=product)
        self.assertEqual('application/json', response.content_type)

    def test_get_one_seller_return_code_200(self):
        response = self.client.get('/seller/1')
        self.assertEqual(200, response.status_code)

    def test_get_one_seller_return_json(self):
        response = self.client.get('/seller/1')
        self.assertEqual('application/json', response.content_type)


    def test_save_new_seller_return_code_200(self):
        seller = { 'nome':'celular'}
        response = self.client.post('/seller/add', json=seller)
        self.assertEqual(201, response.status_code)

    def test_save_new_seller_return_code_200(self):
        seller = { 'nome':'celular'}
        response = self.client.post('/seller/add', json=seller)
        self.assertEqual('application/json', response.content_type)                                       



  


if __name__ == '__main__':
    unittest.main()