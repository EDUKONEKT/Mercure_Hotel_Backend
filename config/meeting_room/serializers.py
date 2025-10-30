import datetime
from datetime import datetime as dt, timedelta
from decimal import Decimal
from rest_framework import serializers
from meeting_room.models import MeetingRoom, MeetingRoomBooking


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['id', 'flour', 'number', 'max_pers', 'type', 'is_available', 'price']


class MeetingRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoomBooking
        fields = [
            'id',
            'meeting_room',
            'account',
            'date',
            'start_time',
            'end_time',
            'total_price',
            'is_deleted',
            'created_at',
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        meeting_room = data['meeting_room']
        date_ = data['date']
        start_time = data['start_time']
        end_time = data['end_time']

       
        if date_ < datetime.date.today():
            raise serializers.ValidationError("La date ne peut pas être dans le passé.")
       
        if start_time >= end_time:
            raise serializers.ValidationError("L'heure de fin doit être après l'heure de début.")
        
        if not meeting_room.is_available:
            raise serializers.ValidationError("Cette salle n'est pas disponible pour le moment.")
        
        if meeting_room.max_pers <= 0:
            raise serializers.ValidationError("Cette salle n'accepte plus de réservations.")
        return data

    def create(self, validated_data):
        meeting_room = validated_data['meeting_room']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        
        duration = (
            dt.combine(datetime.date.today(), end_time)
            - dt.combine(datetime.date.today(), start_time)
        ).seconds / 3600.0

    
        price_float = float(meeting_room.price)
        total = Decimal(duration * price_float).quantize(Decimal('0.01'))

        validated_data['total_price'] = total
        return super().create(validated_data)
