from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from authapp.models import ShopUser, ShopUserProfile
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={'email': user.email,
                                                 'activation_key': user.activation_key})

    title = 'Подтверждение учетной записи {}'.format(user.username)

    message = 'Для подтверждения учетной записи {username} на портале \
{domain} перейдите по ссылке: \n{domain}{link}'.format(
        username=user.username,
        domain=settings.DOMAIN_NAME,
        link=verify_link)

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    title = 'вход'
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        login_form = ShopUserLoginForm()

    content = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('email confirmation send')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('email confirmation error')
                return HttpResponseRedirect(reverse('main:index'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


@transaction.atomic
def edit(request):
    title = 'редактирование'

    user_profile = ShopUserProfile.objects.filter(user=request.user).first()
    if user_profile is None:
        user_profile = ShopUserProfile.objects.create(user_id=request.user.id)

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=user_profile)

    content = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}

    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))

