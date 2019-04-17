from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):

    """login with email or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
#         if '@' in username:
#             kwargs = {'email': username}
#         else:
#             kwargs = {'username': username}
        # login with email 
        if '@' in username:
            kwargs = {'email': username}        
            try:
                user = get_user_model().objects.get(**kwargs)
                if user.check_password(password):
                    return user
            except get_user_model().DoesNotExist:
                return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
