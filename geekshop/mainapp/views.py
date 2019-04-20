import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Product, ProductCategory

# Create your views here.
LIMIT = 3


def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True)
    return random.choice(products)


def get_same_products(product_hot):
    same_products = product_hot.category.product_set.exclude(pk=product_hot.pk)[:LIMIT]
    return same_products


def get_categories_active():
    return ProductCategory.objects.filter(is_active=True)


def index(request):
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'page_title': 'Главная',
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/index.html', context=context)


def catalog(request, page=1):
    title = 'Каталог'
    categories = get_categories_active()
    products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
    paginator = Paginator(products, 3)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'page_title': title,
        'categories': categories,
        'products': products,
    }

    return render(request, 'mainapp/catalog.html', context=context)


def category(request, pk, page=1):
    if int(pk) == 0:
        return HttpResponseRedirect(reverse('main:catalog'))
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.filter(is_active=True)
        categories = get_categories_active()
        paginator = Paginator(products, 3)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'Товары в категории',
        'categories': categories,
        'products': products,
    }
    return render(request, 'mainapp/catalog.html', context=context)


def product(request, pk):
    item = Product.objects.filter(pk=pk).first()
    if not item is None:
        context = {
            'page_title': item.name,
            'product': item,
        }
        return render(request, 'mainapp/product.html', context=context)
    else:
        return HttpResponseRedirect(reverse('main:catalog'))


def contacts(request):
    context = {
        'page_title': 'Контакты',
    }
    return render(request, 'mainapp/contacts.html', context=context)
