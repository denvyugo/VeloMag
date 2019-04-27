# from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    # ShopUserProfile.objects.create(user_id=user.id)
    if backend.name == 'vk-oauth2':
        print('vk-oauth2 keys:', response.keys())
        if 'email' in response.keys():
            user.email = response['email']

        user.save()
