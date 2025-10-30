from rest_framework import viewsets
from car_rent.models import Car_rent, CarRentBooking
from car_rent.serializers import CarRentSerializer, CarBookingSerializer
from rest_framework  import permissions
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsAdmin,IsClient,IsOwnerOrReadOnly,IsReceptionist


class CarRentViewSet(viewsets.ModelViewSet):
    queryset = Car_rent.objects.all()
    serializer_class = CarRentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]  
        else:
            permission_classes = [IsAuthenticated & IsAdmin]  
        return [perm() for perm in permission_classes]

class CarRentBookingViewSet(viewsets.ModelViewSet):
    queryset = CarRentBooking.objects.all()
    serializer_class = CarBookingSerializer  
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

# Create your views here.
