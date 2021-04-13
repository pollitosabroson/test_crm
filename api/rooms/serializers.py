import logging

from rest_framework import serializers
from rooms.models import Room

logger = logging.getLogger(__name__)


class RoomSerializer(serializers.ModelSerializer):
    """List hotel Serializer"""

    code = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('name', 'code')

    def get_code(self, obj):
        return obj.get('public_id')


class CreateRoomSerializer(serializers.ModelSerializer):
    """List room Serializer"""

    class Meta:
        model = Room
        fields = ('name', )

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        values = super(CreateRoomSerializer, self).to_representation(instance)
        # Add Code for return to create valu
        values['code'] = instance.public_id
        return values

    def create(self, validated_data):
        room = Room.objects.create(
            name=validated_data.get('name'),
            hotel_id=validated_data.get('hotel'),
        )
        return room
