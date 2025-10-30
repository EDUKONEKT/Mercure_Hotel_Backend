from rest_framework import permissions
from accounts.models import AccountType

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée :
    - Lecture autorisée pour tous les utilisateurs authentifiés
    - Modification/suppression autorisées uniquement au propriétaire
    """

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Pour les requêtes d'écriture (POST, PUT, PATCH, DELETE)
        # On vérifie que le user connecté est le propriétaire
        owner_field = getattr(obj, 'account', None) or getattr(obj, 'user', None)
        return owner_field == request.user


# ─────────────────────────────────────────────
#   PERMISSIONS BASÉES SUR LES RÔLES (Account)
# ─────────────────────────────────────────────

class IsClient(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs dont le type de compte est 'Client'
    """
    def has_permission(self, request, view):
        # Vérifie que l'utilisateur a un compte lié et de type 'Client'
        return hasattr(request.user, 'account') and request.user.account.type == AccountType.CLIENT


class IsReceptionist(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs dont le type de compte est 'Receptionist'
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'account') and request.user.account.type == AccountType.RECEPTIONIST


class IsAdmin(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs dont le type de compte est 'Admin'
    OU le staff Django standard (is_staff)
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return hasattr(request.user, 'account') and request.user.account.type == AccountType.ADMIN
