import datetime
from decimal import Decimal
from rest_framework import serializers
from restaurant.models import Meal, MealBooking


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'type', 'is_available', 'price']


class MealBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealBooking
        fields = [
            'id',
            'meal',
            'account',
            'date',
            'quantity',
            'total_price',
            'is_deleted',
            'created_at',
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        meal = data['meal']
        date_ = data['date']
        quantity = data.get('quantity', 1)

        # ✅ Date future uniquement
        if date_ < datetime.date.today():
            raise serializers.ValidationError("La date ne peut pas être dans le passé.")

        # ✅ Repas disponible
        if not meal.is_available:
            raise serializers.ValidationError("Ce repas n'est pas disponible pour le moment.")

        # ✅ Quantité positive
        if quantity <= 0:
            raise serializers.ValidationError("La quantité doit être supérieure à 0.")
        return data

    def create(self, validated_data):
        meal = validated_data['meal']
        quantity = validated_data.get('quantity', 1)

        # 💰 Calcul automatique du prix total
        total = Decimal(float(meal.price) * quantity)
        validated_data['total_price'] = total

        return super().create(validated_data)
