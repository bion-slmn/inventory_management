from .views import ItemView, SupplierView
from django.urls import path


urlpatterns = [
    path('view-items/', ItemView.as_view(), name='view_items'),
    path('add-item/', ItemView.as_view(), name='add_item'),
    path('update-item/<str:item_id>', ItemView.as_view(), name='update_item'),
    path('delete-item/<str:item_id>', ItemView.as_view(), name='delete_item'),

    path('view-suppliers/', SupplierView.as_view(), name='view_suppliers'),
    path('add-supplier/', SupplierView.as_view(), name='add_supplier'),
    path(
        'update-supplier/<str:supplier_id>', SupplierView.as_view(), name='update_supplier'),
    path(
        'delete-supplier/<str:supplier_id>', SupplierView.as_view(), name='delete_supplier'),
]