from rest_framework import serializers
from rooms.models import Room, RoomBooking
import datetime


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'name', 'type', 'is_available', 'price']


class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = [
            'id',
            'room',
            'account',
            'check_in',
            'check_out',
            'total_price',
            'is_deleted',
            'created_at',
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        check_in = data['check_in']
        check_out = data['check_out']
        room = data['room']

        if check_in >= check_out:
            raise serializers.ValidationError("La date de départ doit être après la date d'arrivée.")

        if check_in < datetime.date.today():
            raise serializers.ValidationError("La date d'arrivée ne peut pas être dans le passé.")

        if room and not room.is_available:
            raise serializers.ValidationError("Cette chambre n'est pas disponible pour le moment.")

        return data

    def create(self, validated_data):
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        duration = (check_out - check_in).days or 1
        validated_data['total_price'] = duration * room.price
        return super().create(validated_data)