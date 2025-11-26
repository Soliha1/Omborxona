
from django.contrib import admin
from django.urls import path, include
from main.views import *
from users.views import *
from stats.views import *

from users import urls as users_urls

urlpatterns = [
    path('statistics/', include('stats.url')),
    path('sales/<int:pk>/update',Sales_update_view, name='sales-update'),
    path('admin/', admin.site.urls),
    path('sections/', SectionsView.as_view(), name='sections'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete', Products_delete_view, name='product-delete'),
    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/<int:pk>/update', Client_update_view, name='clients-update'),
    path('clients/<int:id>/delete', Clients_delete_view, name='clients-delete'),
    path('login/', LoginView.as_view(), name='login'),
    path('', logout_view, name='logout')

]
