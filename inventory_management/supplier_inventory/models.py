from django.db import models
import uuid

# Create your models here.


class BaseModel(models.Model):
    """
    An abstract base model for other models to
    inherit common fields from.

    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70)

    class Meta:
        abstract = True

class Item(BaseModel):
    """
    A model representing an item in the inventory.
    """
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} at {self.price} '

class Supplier(BaseModel):
    """
    A model representing a supplier in the inventory system.
    """
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(null=True)
    items = models.ManyToManyField(Item, related_name='suppliers')

    def __str__(self) -> str:
        return f'{self.name} - {self.phone_number}'
