import logging

from django.conf import settings
from hotels.models import Hotel
from inventories.models import Inventory
from rates.models import Rate
from rest_framework import serializers
from rooms.models import Room

logger = logging.getLogger(__name__)


class CreateInventorySerializer(serializers.Serializer):
    """Create Inventory Serializer."""

    date = serializers.DateField()
    room = serializers.CharField(
        max_length=settings.LONG_PUBLIC_ID
    )
    hotel = serializers.CharField(
        max_length=settings.LONG_PUBLIC_ID
    )
    price = serializers.DecimalField(
        max_digits=8,
        decimal_places=5,
    )
    name = serializers.CharField()

    def validate_hotel(self, value):
        """Validate hotel exists.
        Args:
            value(str): Hotel code
        Return:
            Dict: Dict with caches values
        """
        hotel = Hotel()
        instance = hotel.get_value_by_id(
            value
        )
        if not instance:
            raise serializers.ValidationError("Hotel don't not exists")
        return instance

    def validate(self, data):
        """
        Check that start is before finish.
        """
        room = Room()
        room_value = room.get_value_by_id(
            data.get('room'),
            nested_id=data.get('hotel', {}).get("public_id")
        )
        if not room_value:
            raise serializers.ValidationError(
                {
                    'room': "room don't not exists"
                }
            )
        filter_rate = Rate.objects.filter(
            inventory__date=data.get('date'),
            room__public_id=data.get('room')
        )
        if filter_rate.exists():
            raise serializers.ValidationError(
                {
                    'date': (
                        'It already exists in the inventory in the room '
                        'on this date'
                    )
                }
            )
        data['room'] = room_value
        return data

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        data = {
            'date': instance.get('date'),
            'room': instance.get('room').get('public_id'),
            'hotel': instance.get('hotel').get('public_id'),
            'price': instance.get('price'),
            'name': instance.get('name'),
        }
        return data

    def save(self, **kwargs):
        """Override save."""
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        obj, _ = Inventory.objects.get_or_create(
            date=validated_data.get('date')
        )
        rate = Rate(
            price=validated_data['price'],
            room_id=validated_data['room'].get('id'),
            inventory=obj,
            name=validated_data['name']
        )
        rate.save()
        return rate
