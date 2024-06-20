http://127.0.0.1:8000/api/view-items/?item_id=c5b72c43-24cd-4a25-bf38-08ec20bc2489

http://127.0.0.1:8000/api/view-items/


curl localhost:8000/api/add-item/ -H 'Content-Type: application/json' -d '{"name": "bike", "description": "bajaj", "price": 23232, "suppliers": ["8057b527-d7b2-4074-8f9a-65a5bdba0d28"]}'


curl localhost:8000/api/update-item/c0bd85f0-ed34-4ce0-a435-6b172865e2bf -H 'Content-Type: application/json' -d '{"name": "Desktop", "description": "computer", "price": 23232}' -X PUT

curl localhost:8000/api/delete-item/c0bd85f0-ed34-4ce0-a435-6b172865e2bf  -X DELETE

http://127.0.0.1:8000/api/view-suppliers/?supplier_id=8057b527-d7b2-4074-8f9a-65a5bdba0d28


http://127.0.0.1:8000/api/view-suppliers/

