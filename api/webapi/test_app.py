from unittest import mock, TestCase
from app import webapp
import json


class TestApp(TestCase):
    def setUp(self):
      self.client = webapp.test_client()

    def test_init_return_code_200(self):
        response = self.client.get('/app')
        self.assertEqual(200, response.status_code)  

    def test_get_client_from_id_return_code_200(self):
        # o codigo de status deve ser 200
        response = self.client.get('/app/client/3')
        self.assertEqual(200, response.status_code)

    def test_get_client_from_id_return_json(self):
        # quando acessar /client/1 é esperado um objeto json
        response = self.client.get('/app/client/3')
        self.assertEqual('application/json', response.content_type)    

    # @mock.patch('app.create_new_client_db')
    def test_insert_new_client_return_code_201(self):
        client = { 'nome': 'Valdir' }
        response = self.client.post('/app/client/add', json=client)
        self.assertEqual(201, response.status_code)

    # @mock.patch('app.create_new_client_db')
    def test_insert_new_client_return_json(self):
        client = { 'nome': 'Jose' }
        response = self.client.post('/app/client/add', json=client)
        self.assertEqual('application/json', response.content_type)

    def test_get_all_clients_return_code_200(self):
        response = self.client.get('/app/clients/')
        self.assertEqual(200, response.status_code)

    def test_get_all_clients_return_json(self):
        response = self.client.get('/app/clients/')
        self.assertEqual('application/json', response.content_type) 

    def test_get_products_return_code_200(self):
        response = self.client.get('/app/product/Celular')
        self.assertEqual(200, response.status_code) 

    def test_get_products_return_json(self):
        response = self.client.get('/app/product/Celular')
        self.assertEqual('application/json', response.content_type)

    def test_save_new_product_return_code_200(self):
        product = { 'nome':'celular'}
        response = self.client.post('/app/product/add', json=product)
        self.assertEqual(201, response.status_code)

    def test_save_new_product_return_code_200(self):
        product = { 'nome':'celular'}
        response = self.client.post('/app/product/add', json=product)
        self.assertEqual('application/json', response.content_type)

    def test_get_one_seller_return_code_200(self):
        response = self.client.get('/app/seller/1')
        self.assertEqual(200, response.status_code)

    def test_get_one_seller_return_json(self):
        response = self.client.get('/app/seller/1')
        self.assertEqual('application/json', response.content_type)

        
    def test_get_all_seller_return_code_200(self):
        response = self.client.get('/app/seller/')
        self.assertEqual(200, response.status_code)

    def test_get_all_seller_return_json(self):
        response = self.client.get('/app/seller/')
        self.assertEqual('application/json', response.content_type)


    def test_save_new_seller_return_code_200(self):
        seller = { 'nome':'celular'}
        response = self.client.post('/app/seller/add', json=seller)
        self.assertEqual(201, response.status_code)

    def test_save_new_seller_return_json(self):
        seller = { 'nome':'celular'}
        response = self.client.post('/app/seller/add', json=seller)
        self.assertEqual('application/json', response.content_type)

    def test_save_sales_return_code_200(self):
        sales = { "vendedor": 'valdir', 'cliente': 'mauricio', 'subtotal': '200'}
        response = self.client.post('/app/sales_list/add', json=sales)
        self.assertEqual(200, response.status_code)

    def test_save_sales_return_json(self):
        sales = { "vendedor": 'valdir', 'cliente': 'mauricio', 'subtotal': '200'}
        response = self.client.post('/app/sales_list/add', json=sales)
        self.assertEqual('application/json', response.content_type)

    def test_get_seller_comission_return_code_200(self):
        response = self.client.get('/app/seller/Valdir')
        self.assertEqual(200, response.status_code)

    def test_get_seller_comission_return_json(self):
      
        response = self.client.get('/app/seller/Valdir')
        self.assertEqual('application/json', response.content_type)                                              



  


if __name__ == '__main__':
    unittest.main()