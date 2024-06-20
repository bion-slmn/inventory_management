from django.http import HttpRequest
from rest_framework.response import Response
from .models import Item, Supplier
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serialiser import ItemSerialiser, SupplierSerialiser
from typing import List, Type
from django.db.models import Model
import json



def check_ids(object_ids: List[int], obj_class: Type[Model]) -> int:
    """
    Check if all object IDs are present in the database.

    Args:
        object_ids (list): List of object IDs to check.
        obj_class (Model): Model class to query for object IDs.

    Returns:
        bool: True if all object IDs are present, False otherwise.
    """
    return obj_class.objects.filter(id__in=object_ids).count() == len(object_ids)


def update_object(object_data: dict, obj):
    updated = False
    for key, value in object_data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
            updated = True
    return updated



class ApiMethodMixin:
    def update(self, request: HttpRequest, obj) -> str:
        
        data_copy = request.data.copy()
        if not data_copy:
            return {'error': "No data passed"}

        related_ids = data_copy.pop(self.related_name, [])
        updated = update_object(data_copy, obj)

        if related_ids:
            if not check_ids(related_ids, self.related_model):
                return {"error": "Some Supplier IDs do not exist"}
            getattr(obj, self.related_name).add(*related_ids)

            updated = True

        return None if updated else {'error': "Nothing to update"}
            

class ItemView(APIView, ApiMethodMixin):
    """
    Handles GET, POST, PUT, and DELETE requests for item details
    and associated suppliers.
    """
    related_model = Supplier
    model = Item
    related_name = 'suppliers'
    def get(self, request: HttpRequest) -> Response:
        """
        Handles GET requests to retrieve item details and associated suppliers.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: JSON response containing item details and associated suppliers
            or all items if no specific item ID is provided.
        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        item_id = request.query_params.get('item_id')
        try:
            if not item_id:
                all_items = Item.objects.all()
                all_items_json = ItemSerialiser(all_items, many=True).data
                return Response(all_items_json)

            item = get_object_or_404(
                Item.objects.prefetch_related('suppliers'), id=item_id)

            item_json = ItemSerialiser(item).data
            all_suppliers = item.suppliers.all().values('id', 'name', 'phone_number')
            combined_data = {'item': item_json, 'suppliers': all_suppliers}
            return Response(combined_data)
        
        except Exception as error:
            return Response(f'Error: {error}', 400)

    def post(self, request: HttpRequest) -> Response:
        """
        Handle POST requests to create a new item with
        associated suppliers.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: JSON response with the created
            item details and associated suppliers.
            Raises:
                Exception: If an error occurs during the creation process.
        """
        try:
            suppliers_ids = request.data.get('suppliers')
            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')

            if not suppliers_ids:
                return Response(
                    {"Error": "Please add the supplier"}, status=400)

            if not check_ids(suppliers_ids, Supplier):
                return Response(
                    {"error": "Some Supplier IDs do not exist"}, 400)

            item = Item.objects.create(
                name=name, description=description, price=price)
            item.suppliers.add(*suppliers_ids)
            return Response(f'Item_id: {item.id}, {str(item)}', 201)
        
        except Exception as error:
            return Response(f'Error: {error}', 400)

    def put(self, request: HttpRequest, item_id: str) -> Response:
        """
        Handle PUT requests to update an existing item
        with new details and associated suppliers.

        Args:
            request (HttpRequest): The HTTP request object.
            item_id (str): The ID of the item to update.

        Returns:
            Response: JSON response with the updated item details.
            Raises:
                Exception: If an error occurs during the update process.
        """
        try:
            item = get_object_or_404(Item, id=item_id)
            if result := self.update(request, item):
                return Response(result, 400)

            item.save()
            return Response(f'items_id: {item.id}, {str(item)} updated')

        except Exception as error:
            return Response(f'Error: {error}', 400)

    def delete(self, request: HttpRequest, item_id: str) -> Response:
        """
        Handle DELETE requests to remove an item from the database.

        Args:
            request (HttpRequest): The HTTP request object.
            item_id (str): The ID of the item to delete.

        Returns:
            Response: JSON response confirming the deletion of the item.
            Raises:
                Exception: If an error occurs during the deletion process.
        """
        try:
            item = get_object_or_404(Item, id=item_id)
            item_details = str(item)
            item.delete()
            return Response(f'{item_details} deleted')
        except Exception as error:
            return Response(f'Error: {error}', 400)


class SupplierView(APIView, ApiMethodMixin):
    """
    Handles GET, POST, and PUT requests for supplier details and
    associated items.
    """
    related_model = Item
    model = Supplier
    related_name = 'items'
    def get(self, request: HttpRequest) -> Response:
        """
        Handle GET requests to retrieve supplier details and associated items.
        
        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: JSON response containing supplier details and associated items
            or all suppliers if no specific supplier ID is provided.
            Raises:
                Exception: If an error occurs during the retrieval process.
        """

        supplier_id = request.query_params.get('supplier_id')
        try:
            if supplier_id:
                supplier = get_object_or_404(Supplier, id=supplier_id)
                serialiser = SupplierSerialiser(supplier)
                return Response(serialiser.data)
            
            all_suppliers = Supplier.objects.all().values(
                'id', 'name', 'phone_number', 'email'
            )
            return Response(all_suppliers)
        except Exception as error:
            return Response(f'Error: {error}', 400)

    def post(self, request: HttpRequest) -> Response:
        """
        Handle POST requests to create a new supplier
        with associated items.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: JSON response with the created supplier details.
            Raises:
                Exception: If an error occurs during the creation process.
        """
        try:
            name = request.data.get('name')
            phone_number = request.data.get('phone_number')
            email = request.data.get('email')
            items_ids = request.data.get('items')

            supplier = Supplier.objects.create(
                name=name, phone_number=phone_number, email=email)
            
            if items_ids:
                if isinstance(items_ids, str):
                    items_ids = items_ids.split(', ')
                if not check_ids(items_ids, Item):
                    return Response('Some id of items dont exist', 400)
                supplier.items.add(*items_ids)
            serialiser = SupplierSerialiser(supplier)
            return Response(serialiser.data, 201)

        except Exception as error:
            return Response(f'Error: {error}', 400)

    def put(self, request: HttpRequest, supplier_id: str) -> Response:
        """
        Handle PUT requests to update an existing supplier
        with new details and associated items.

        Args:
            request (HttpRequest): The HTTP request object.
            supplier_id (str): The ID of the supplier to update.

        Returns:
            Response: JSON response with the updated supplier details.
            Raises:
                Exception: If an error occurs during the update process.
        """
        try:
            supplier = get_object_or_404(Supplier, id=supplier_id)
            if result := self.update(request, supplier):
                return Response(result, 400)
            
            supplier.save()
            serialiser = SupplierSerialiser(supplier)
            return Response(serialiser.data)

        except Exception as error:
            return Response(f'Error: {error}', 400)


