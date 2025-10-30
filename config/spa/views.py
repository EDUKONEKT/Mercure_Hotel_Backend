from rest_framework import viewsets
from rest_framework import permissions
from spa.models import Spa, SpaBooking
from spa.serializers import SpaSerializer, SpaBookingSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsAdmin , IsReceptionist ,IsClient, IsOwnerOrReadOnly

class SpaViewSet(viewsets.ModelViewSet):
    queryset = Spa.objects.all()
    serializer_class = SpaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]  
        else:
            permission_classes = [IsAuthenticated & IsAdmin]  
        return [perm() for perm in permission_classes]

class SpaBookingViewSet(viewsets.ModelViewSet):
    queryset = SpaBooking.objects.all()
    serializer_class = SpaBookingSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsReceptionist | (IsClient & IsOwnerOrReadOnly))]

    def perform_create(self, serializer):
        user = self.request.user
        account = None

        # ✅ Cas 1 : Client connecté → pour lui-même
        if hasattr(user, "account") and user.account.type == "Client":
            account = user.account

        # ✅ Cas 2 : Réceptionniste ou Admin → account fourni dans le body
        elif hasattr(user, "account") and user.account.type in ["Admin", "Receptionist"]:
            account = serializer.validated_data.get("account",None)

        # ✅ Cas 3 : Visiteur non connecté → pas de compte
        else:
            account = None

        serializer.save(account=account)