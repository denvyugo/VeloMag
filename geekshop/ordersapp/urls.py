"""ordersapp URL Configuration

"""
from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('order/create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
]
