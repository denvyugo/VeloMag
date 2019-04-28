"""ordersapp URL Configuration

"""
from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('order/create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>/', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('order/detail/<int:pk>', ordersapp.OrderDetail.as_view(), name='order_detail'),
    path('order/order_forming_complete/<int:pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
]
