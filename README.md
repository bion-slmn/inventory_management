# INVENTORY - SUPPLIER MANAGEMENT APP

This project involves creating an inventory and supplier app using django.
The Inventory is called item and supplier is called a Supplier in this app
An Item can have many suppliers and a supplier can have many items.
EVery item must have atleast one supplier

The directory of the app is called  supplier_inventory

### START APP

TO start the app install the libraries required
```
pip install -r requirements.txt
```
Move to project directory using
```
cd inventory_management/inventory_management
```
### Start django server using
```
python3 manange.py runserver
```

All API's return data in json format
### View all items user
This will show all items without their suppliers
```
http://127.0.0.1:8000/api/view-items/
```
Return a list of all items a shown
```
[
    {
        "id": "0c79132c-d12f-4fa0-900d-869f3d5c5bfc",
        "created_at": "2024-06-19 05:30:34",
        "name": "phone",
        "description": "tecno is gd",
        "price": "12.00"
    },
    {
        "id": "ba0c65ea-bc86-43a8-afab-48a2ba15ac61",
        "created_at": "2024-06-19 05:30:58",
        "name": "phone2",
        "description": "tecno is bad",
        "price": "1233.00"
    }
]
```

### View an item plus its suppliers
This show all details including suppliers of the item
This supplier is a list of all suppliers

```
http://127.0.0.1:8000/api/view-items/?item_id=c5b72c43-24cd-4a25-bf38-08ec20bc2489
```
### Returns
```
{
    "item": {
        "id": "c5b72c43-24cd-4a25-bf38-08ec20bc2489",
        "created_at": "2024-06-19 07:20:45",
        "name": "bike",
        "description": "tvs",
        "price": "23232.00"
    },
    "suppliers": [
        {
            "id": "8057b527-d7b2-4074-8f9a-65a5bdba0d28",
            "name": "bon",
            "phone_number": "002323232"
        }
    ]
}
```
### Adding an item

```
curl localhost:8000/api/add-item/ -H 'Content-Type: application/json' -d '{"name": "bike", "description": "bajaj", "price": 23232, "suppliers": ["8057b527-d7b2-4074-8f9a-65a5bdba0d28"]}'
```

Return 
```
"Item_id: bd08b459-5b08-40fc-ba94-bf112d81c13b, bike at 23232 "
```

### Updating and item
```
curl localhost:8000/api/update-item/c0bd85f0-ed34-4ce0-a435-6b172865e2bf -H 'Content-Type: application/json' -d '{"name": "Desktop", "description": "computer", "price": 23232}' -X PUT
```

### Deleting and item
```
curl localhost:8000/api/delete-item/c0bd85f0-ed34-4ce0-a435-6b172865e2bf  -X DELETE
```

http://127.0.0.1:8000/api/view-suppliers/?supplier_id=8057b527-d7b2-4074-8f9a-65a5bdba0d28


http://127.0.0.1:8000/api/view-suppliers/

