from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from mainapp.models import Product
from .models import Basket


# Create your views here.
@login_required
def index(request):
    title = 'Корзина'
    items = request.user.basket.order_by('add_datetime')
    context = {
        'page_title': title,
        'basket': items
    }

    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product', kwargs={'pk': pk}))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if basket:
        if basket.quantity > 1:
            basket.quantity -=1
            basket.save()
        else:
            basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def delete(request, pk):
    basket = get_object_or_404(Basket, pk)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def update(request, pk, quantity):
    if request.is_ajax():
        basket_item = get_object_or_404(Basket, pk=int(pk))
        quantity = int(quantity)
        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        context = {
            'basket': request.user.basket.order_by('add_datetime')
        }

        result = render_to_string('basketapp/includes/inc__basket_list.html', context)

        return JsonResponse({
            'result': result
        })
