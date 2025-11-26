from django.urls import path
from .views import *
urlpatterns=[
    path('sales/', SalesView.as_view(), name='sales'),
    path('sales/<int:id>/delete', Sales_delete_view, name='sales-delete'),
    path('products/', ImportProductsView.as_view(), name='imports'),
    path('products/<int:id>/delete', Imports_delete_view, name='imports-delete'),
    path('client-debt/', PaydebtsView.as_view(), name='pay-debt'),
    path('client-debt/<int:pk>/edit', Paydebt_edit_view, name='paydebt_edit'),
    path('client-debt/<int:id>/delete', Paydebt_delete_view, name='paydebt_delete')
]
