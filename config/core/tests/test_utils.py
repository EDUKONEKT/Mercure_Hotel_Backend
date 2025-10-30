from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Account, AccountType

def create_user_with_role(username, role):
    user = User.objects.create_user(username=username, password='pass1234')
    Account.objects.create(user=user, type=role)
    return user

def get_auth_headers(user):
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}
