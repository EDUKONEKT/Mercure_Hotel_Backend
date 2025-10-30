# Create your views here.
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsAdmin
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated & IsAdmin]
