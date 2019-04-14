from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from .forms import ShopUserCreationAdminForm, ShopUserUpdateAdminForm
from .forms import ProductCategoryCreateAdminForm, ProductCreateAdminForm


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    title = 'уравление/пользователи'
    objects = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'objects': objects
    }
    return render(request, 'adminapp/index.html', context=context)


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    title = 'управление/новый пользователь'
    if request.method == 'POST':
        form = ShopUserCreationAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserCreationAdminForm()

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/shopuser_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    title = 'управление/редактировать пользователя'
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserUpdateAdminForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserUpdateAdminForm(instance=current_user)

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/shopuser_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    title = 'управление/удалить пользователя'
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('myadmin:index'))

    context = {
        'title': title,
        'user_to_delete': current_user
    }
    return render(request, 'adminapp/shopuser_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    title = 'управление/категории'
    object_list = ProductCategory.objects.all()
    context = {
        'title': title,
        'object_list': object_list
    }
    return render(request, 'adminapp/productcategory_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_create(request):
    title = 'управление/новая категория'
    if request.method == 'POST':
        form = ProductCategoryCreateAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = ProductCategoryCreateAdminForm()

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/productcategory_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_update(request, pk):
    title = 'управление/категория'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryCreateAdminForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = ProductCategoryCreateAdminForm(instance=category)

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/productcategory_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_delete(request, pk):
    title = 'управление/удалить категорию'
    category_to_delete = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_to_delete.is_active = False
        category_to_delete.save()
        return HttpResponseRedirect(reverse('myadmin:categories'))

    context = {
        'title': title,
        'category_to_delete': category_to_delete
    }
    return render(request, 'adminapp/productcategory_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def products(request, pk):
    title = 'управление/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all().order_by('name')
    context = {
        'title': title,
        'category': category,
        'object_list': object_list
    }
    return render(request, 'adminapp/product_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request, pk):
    title = 'управление/новый продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCreateAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': pk}))
    else:
        form = ProductCreateAdminForm(initial={'category': category})

    context = {
        'title': title,
        'category': pk,
        'form': form
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, pk):
    title = 'управление/продукт'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductCreateAdminForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': product.category.pk}))
    else:
        form = ProductCreateAdminForm(instance=product)

    context = {
        'title': title,
        'category': product.category.pk,
        'form': form
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    title = 'управление/удалить продукт'
    product_to_delete = get_object_or_404(Product, pk=pk)
    category = product_to_delete.category
    if request.method == 'POST':
        product_to_delete.is_active = False
        product_to_delete.save()
        return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': category.pk}))

    context = {
        'title': title,
        'product_to_delete': product_to_delete,
        'category': category
    }
    return render(request, 'adminapp/product_delete.html', context)
