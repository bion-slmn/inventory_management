from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from supplier_inventory.models import Item, Supplier
import json

class ItemViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.supplier1 = Supplier.objects.create(name="Supplier1", phone_number="1234567890")
        self.supplier2 = Supplier.objects.create(name="Supplier2", phone_number="0987654321")
        self.item1 = Item.objects.create(name="Item1", description="Description1", price=100)
        self.item1.suppliers.add(self.supplier1, self.supplier2)

    def test_get_all_items(self):
        url = reverse('view_items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertIsInstance(response.data, list)

    def test_response(self):
        url = reverse('view_items')
        response = self.client.get(url)
        first_response = response.data[0]

        self.assertEqual(first_response['name'], "Item1")
        self.assertEqual(first_response['description'], "Description1")
        self.assertEqual(float(first_response['price']), 100.00)
        self.assertIsNone(first_response.get('suppliers'))


    def test_get_item_details_single_item(self):
        base_url = reverse('view_items')
        url = f"{base_url}?item_id={self.item1.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

    
    def test_single_item_data(self):
        base_url = reverse('view_items')
        url = f"{base_url}?item_id={self.item1.pk}"
        response = self.client.get(url)

        self.assertEqual(response.data['item']['name'], "Item1")
        self.assertEqual(response.data['item']['description'], "Description1")
        self.assertEqual(float(response.data['item']['price']), 100.00)
        self.assertTrue(response.data.get('suppliers'))
    
    def test_get_invalid_item_details(self):
        base_url = reverse('view_items')
        url = f"{base_url}?item_id=0000"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
    

    def test_create_item_successful(self):
        url = reverse('add_item')
        payload = {"name": "bike", "description": "bajaj", "price": 23232, "suppliers": [self.supplier1.id]}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_item_data(self):
        url = reverse('add_item')
        payload = {"name": "bike", "description": "bajaj", "price": 23232, "suppliers": [self.supplier1.id]}
        response = self.client.post(url, data=payload, format='json')
        self.assertIn('Item_id', response.data)
        self.assertIn('bike', response.data)
        self.assertIn('23232', response.data)
        
    def test_create_item_missing_suppliers(self):
        url = reverse('add_item')
        payload = {"name": "bike", "description": "bajaj", "price": 23232}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], 'Please add the supplier')

    def test_create_item_invalid_suppliers(self):
        url = reverse('add_item')
        payload = {"name": "bike", "description": "bajaj", "price": 23232, "suppliers": [12122]}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Some Supplier IDs do not exist')

    def test_create_item_no_name(self):
        # ivalid name
        url = reverse('add_item')
        payload = {"description": "bajaj", "price": 23232, "suppliers": [self.supplier1.id]}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_suppliers_not_list(self):
        url = reverse('add_item')
        payload = {"name": "bike", "description": "bajaj", "price": 23232, "suppliers": self.supplier1.id}
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_item_successful_no_supplier(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})
        payload = {'name': 'Phone', 'description': 'New phone', 'price': 150}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, 'Phone')
        self.assertEqual(self.item1.description, 'New phone')
        self.assertEqual(self.item1.price, 150.00)

    def test_update_item_successful_with_supplier(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})
        supplier3 = Supplier.objects.create(name="Supplier2", phone_number="0987654321")
        payload = {'name': 'Phone', 'description': 'New phone', 'price': 150, 'suppliers': [supplier3.id]}
        response = self.client.put(url, data=payload, format='json')
        print(response.data, 11111111111111)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, 'Phone')
        self.assertEqual(self.item1.description, 'New phone')
        self.assertEqual(self.item1.price, 150.00)
        self.assertIn(supplier3, self.item1.suppliers.all())


    def test_update_item_invalid_suppliers(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id}) 
        payload = {'name': 'Phone', 'description': 'New phone', 'price': 150, 'suppliers': [1212121]}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Some Supplier IDs do not exist')

    def test_partial_update_item(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})  # Adjust with your actual URL name
        response = self.client.put(url, data={'description': 'Partially Updated Description'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.description, 'Partially Updated Description')

    def test_update_item_not_found(self):
        url = reverse('update_item', kwargs={'item_id': 'non_existent_id'})  # Adjust with your actual URL name
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_item_emppty_payload(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})
        payload = {}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'No data passed')

    def test_update_item_payload_notupdatable(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})
        payload = {"33333":12121}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Nothing to update')

    def test_delete_item_successful(self):
        url = reverse('delete_item', kwargs={'item_id': self.item1.id})  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Item.objects.filter(id=self.item1.id).exists())

    def test_delete_item_not_found(self):
        url = reverse('delete_item', kwargs={'item_id': 'non_existent_id'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

class SupplierViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.supplier1 = Supplier.objects.create(name="Supplier1", phone_number="1234567890")
        self.supplier2 = Supplier.objects.create(name="Supplier2", phone_number="0987654321")
        self.item1 = Item.objects.create(name="Item1", description="Description1", price=100)
        self.item1.suppliers.add(self.supplier1, self.supplier2)

    def test_get_all_suppliers(self):
        url = reverse('view_suppliers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_get_all_suppliers(self):
        url = reverse('view_suppliers') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        supplier_names = [supplier['name'] for supplier in response.data]
        self.assertIn("Supplier1", supplier_names)
        self.assertIn("Supplier2", supplier_names)

    def test_get_single_supplier(self):
        url = reverse('view_suppliers') 
        response = self.client.get(url, {'supplier_id': self.supplier1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier1.name)
        self.assertEqual(response.data['phone_number'], self.supplier1.phone_number)
        self.assertEqual(response.data['email'], None)
        self.assertTrue(response.data.get('items'))
    
    def test_get_single_supplier_items(self):
        url = reverse('view_suppliers') 
        response = self.client.get(url, {'supplier_id': self.supplier1.id})
        items = response.data.get('items', [])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'Item1')
        self.assertEqual(items[0]['description'], 'Description1')
        self.assertEqual(items[0]['price'], '100.00')

    def test_get_single_supplier_not_found(self):
        url = reverse('view_suppliers')  # Adjust with your actual URL name
        response = self.client.get(url, {'supplier_id': 'non_existent_id'})
        self.assertEqual(response.status_code, 400)
    

class SupplierPostTestCase(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(name="Item1", description="Description1", price="100.00")
        self.item2 = Item.objects.create(name="Item2", description="Description2", price="200.00")

    def test_create_supplier_with_items(self):
        url = reverse('add_supplier') 
        data = {
            "name": "New Supplier",
            "phone_number": "1234567890",
            "email": "newsupplier@example.com",
            "items": [self.item1.id, self.item2.id]
        }
        response = self.client.post(url, data, format='json')
     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])
        self.assertEqual(response.data['email'], data['email'])


    def test_create_supplier_without_items(self):
        url = reverse('add_supplier')  # Adjust with your actual URL name
        data = {
            "name": "New Supplier",
            "phone_number": "1234567890",
            "email": "newsupplier@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(len(response.data['items']), 0)

    def test_create_supplier_with_invalid_item_ids(self):
        url = reverse('add_supplier')
        data = {
            "name": "New Supplier",
            "phone_number": "1234567890",
            "email": "newsupplier@example.com",
            "items": ["non_existent_id"]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SupplierPutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supplier1 = Supplier.objects.create(name="Supplier1", phone_number="1234567890")
        self.supplier2 = Supplier.objects.create(name="Supplier2", phone_number="0987654321")
        self.item1 = Item.objects.create(name="Item1", description="Description1", price=100)
        self.item1.suppliers.add(self.supplier1, self.supplier2)

    def test_update_supplier_successful_no_item(self):
        url = f'/api/update-supplier/{self.supplier1.id}'
        payload = {'name': 'Phone', 'phone_number': '111111111111', 'email':"supplier1@example.com"}
        response = self.client.put(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier1.refresh_from_db()
        self.assertEqual(self.supplier1.name, 'Phone')
        self.assertEqual(self.supplier1.phone_number, '111111111111')
        self.assertEqual(self.supplier1.email, "supplier1@example.com")


    def test_update_supplier_successful_with_items(self):
        url = reverse('update_supplier', kwargs={'supplier_id': self.supplier1.id})
        item3 = Item.objects.create(name="bread", description="sweet with bb", price=122)
        payload = {'items': [item3.id]}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier1.refresh_from_db()
        self.assertEqual(self.supplier1.name, 'Supplier1')
        self.assertEqual(self.supplier1.phone_number, '1234567890')
        self.assertEqual(self.supplier1.email, None)
        self.assertIn(item3, self.supplier1.items.all())


    def test_update_supplier_invalid_item(self):
        url = reverse('update_supplier', kwargs={'supplier_id': self.supplier1.id}) 
        payload = {'items': [1212121]}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier_item_not_found(self):
        url = reverse('update_supplier', kwargs={'supplier_id': 'non_existent_id'})  # Adjust with your actual URL name
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_supplier_emppty_payload(self):
        url = reverse('update_supplier', kwargs={'supplier_id': self.supplier1.id})
        payload = {}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'No data passed')

    def test_update_supplier_payload_notupdatable(self):
        url = reverse('update_item', kwargs={'item_id': self.item1.id})
        payload = {"33333":12121}
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Nothing to update')