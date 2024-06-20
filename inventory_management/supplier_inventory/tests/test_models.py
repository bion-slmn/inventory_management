from django.test import TestCase
from supplier_inventory.models import Item, Supplier
import uuid

class ItemSupplierModelTests(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(
            name="Item1", description="Description1", price="100.00")
        self.item2 = Item.objects.create(
            name="Item2", description="Description2", price="200.00")

        self.supplier1 = Supplier.objects.create(
            name="Supplier1", phone_number="1234567890", email="supplier1@example.com")
        self.supplier2 = Supplier.objects.create(
            name="Supplier2", phone_number="0987654321", email="supplier2@example.com")

    def test_create_item(self):
        item = Item.objects.create(
            name="NewItem", description="NewDescription", price="300.00")
        self.assertEqual(item.name, "NewItem")
        self.assertEqual(item.description, "NewDescription")
        self.assertEqual(float(item.price), 300.00)
        self.assertIsInstance(item.id, uuid.UUID)
        self.assertIsNotNone(item.created_at)

    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="NewSupplier", phone_number="1111111111", email="newsupplier@example.com")
        self.assertEqual(supplier.name, "NewSupplier")
        self.assertEqual(supplier.phone_number, "1111111111")
        self.assertEqual(supplier.email, "newsupplier@example.com")
        self.assertIsInstance(supplier.id, uuid.UUID)

    def test_item_str(self):
        self.assertEqual(str(self.item1), "Item1 at 100.00 ")
        self.assertEqual(str(self.item2), "Item2 at 200.00 ")

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier1), "Supplier1 - 1234567890")
        self.assertEqual(str(self.supplier2), "Supplier2 - 0987654321")

    def test_supplier_items_relationship(self):
        self.supplier1.items.add(self.item1)
        self.supplier1.items.add(self.item2)
        self.assertEqual(self.supplier1.items.count(), 2)
        self.assertIn(self.item1, self.supplier1.items.all())
        self.assertIn(self.item2, self.supplier1.items.all())
        
        self.supplier2.items.add(self.item2)
        self.assertEqual(self.supplier2.items.count(), 1)
        self.assertIn(self.item2, self.supplier2.items.all())
        self.assertNotIn(self.item1, self.supplier2.items.all())

    def test_supplier_with_no_items(self):
        supplier = Supplier.objects.create(
            name="Supplier3", phone_number="2222222222", email="supplier3@example.com")
        self.assertEqual(supplier.items.count(), 0)
