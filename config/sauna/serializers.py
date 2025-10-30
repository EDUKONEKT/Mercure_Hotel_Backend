import datetime
from rest_framework import serializers
from sauna.models import Sauna, SaunaBooking

class SaunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauna
        fields = ['id','name', 'price', 'is_available', 'type']
        

class SaunaBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaunaBooking
        fields = ['id', 'sauna', 'account', 'check_in', 'check_out', 'total_price', 'is_deleted', 'created_at']
        read_only_fields = ['total_price', 'created_at']
    
    def create(self, validated_data):
        sauna = validated_data['sauna']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        duration = (check_out - check_in).days or 1
        validated_data['total_price'] = duration * sauna.price
        return super().create(validated_data)
    

    def validate(self, data):
        if data['check_in'] < datetime.date.today():
         raise serializers.ValidationError("La date de début ne peut pas être dans le passé.")
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("La date de fin doit être après la date de début.")
        if not data['sauna'].is_available:
            raise serializers.ValidationError("Ce sauna n'est pas disponible pour le moment.")
        return data            