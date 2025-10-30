import datetime
from rest_framework import serializers
from car_rent.models import Car_rent, CarRentBooking

class CarRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car_rent
        fields = ['id', 'name', 'qty', 'type', 'is_available', 'price']


class CarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRentBooking
        fields = [
            'id', 'car_rent', 'account',
            'check_in', 'check_out',
            'total_price', 'is_deleted', 'created_at'
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        car = data['car_rent']
        check_in = data['check_in']
        check_out = data['check_out']

        if check_in < datetime.date.today():
            raise serializers.ValidationError("La date de début ne peut pas être dans le passé.")
        if check_in >= check_out:
            raise serializers.ValidationError("La date de fin doit être après la date de début.")
        if not car.is_available or car.qty <= 0:
            raise serializers.ValidationError("Ce véhicule n'est pas disponible pour le moment.")

        
        overlap = CarRentBooking.objects.filter(
            car_rent=car,
            check_out__gt=check_in,
            check_in__lt=check_out
        )
        if overlap.exists():
            raise serializers.ValidationError("Ce véhicule est déjà réservé sur cette période.")
        return data

    def create(self, validated_data):
        car = validated_data['car_rent']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        duration = (check_out - check_in).days or 1
        validated_data['total_price'] = duration * car.price
        return super().create(validated_data)
