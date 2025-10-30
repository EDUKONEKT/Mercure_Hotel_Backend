import datetime
from rest_framework import serializers
from spa.models import Spa, SpaBooking

class SpaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = ['id','name', 'price', 'is_available', 'type']

class SpaBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaBooking
        fields = ['id', 'spa', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted', 'created_at']
        read_only_fields = ['total_price', 'created_at']
    
    def create(self, validated_data):
        spa = validated_data['spa']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        duration = (check_out - check_in).days or 1
        validated_data['total_price'] = duration * spa.price
        return super().create(validated_data)
    

    def validate(self, data):
        if data['check_in'] < datetime.date.today():
         raise serializers.ValidationError("La date de début ne peut pas être dans le passé.")
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("La date de fin doit être après la date de début.")
        if not data['spa'].is_available:
            raise serializers.ValidationError("Ce spa n'est pas disponible pour le moment.")
        return data    
    

    