"""mainapp URL Configuration

"""
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name = 'index'),
    path('products/<int:page>', mainapp.catalog, name='catalog'),
    path('category/<int:pk>/<int:page>', mainapp.category, name='category'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('contacts/', mainapp.contacts, name='contacts'),
]
