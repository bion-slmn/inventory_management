from rest_framework import serializers
from .models import Item, Supplier


class ItemSerialiser(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class SupplierSerialiser(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = ItemSerialiser(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone_number', 'email', 'items']
