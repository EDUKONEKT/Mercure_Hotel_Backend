# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # on autorise l'objet user complet

    class Meta:
        model = Account
        fields = ['id', 'user', 'type']

    def create(self, validated_data):
        # Extraire les données user
        user_data = validated_data.pop('user')
        # Créer un utilisateur Django
        user = User.objects.create_user(**user_data)
        # Créer un Account lié à ce user
        account = Account.objects.create(user=user, **validated_data)
        return account
