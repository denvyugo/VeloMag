"""mainapp URL Configuration

"""
from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.UsersListView.as_view(), name='index'),
    path('user_create/', adminapp.UsersCreateView.as_view(), name='user_create'),
    path('user_update/<int:pk>', adminapp.UsersUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:pk>', adminapp.UsersDeleteView.as_view(), name='user_delete'),
    path('categories/', adminapp.categories, name='categories'),
    path('category_create/', adminapp.category_create, name='category_create'),
    path('category_update/<int:pk>', adminapp.category_update, name='category_update'),
    path('category_delete/<int:pk>', adminapp.category_delete, name='category_delete'),
    path('products/<int:pk>', adminapp.products, name='products'),
    path('product_create/<int:pk>', adminapp.product_create, name='product_create'),
    path('product_update/<int:pk>', adminapp.product_update, name='product_update'),
    path('product_delete/<int:pk>', adminapp.product_delete, name='product_delete')
    # path('edit/', authapp.edit, name='edit'),
]
