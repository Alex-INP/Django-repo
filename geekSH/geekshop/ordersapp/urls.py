from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.views import index, products

from ordersapp.views import OrderList, OrderCreate, OrderUpdate, OrderDelete, OrderRead, OrderItemsCreate, order_forming_complete
from django.urls import re_path

app_name = "ordersapp"

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>/', OrderRead.as_view(), name='read'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming-complete/<int:pk>/', order_forming_complete, name='forming_complete'),

]

