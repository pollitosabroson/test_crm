# -*- coding: utf-8 -*-
import logging

from hotels.models import Hotel
from rest_framework import serializers

logger = logging.getLogger(__name__)


class HotelSerializer(serializers.ModelSerializer):
    """List hotel Serializer"""

    code = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ('name', 'code')

    def get_code(self, obj):
        return obj.get('public_id')


class CreateHotelSerializer(serializers.ModelSerializer):
    """List hotel Serializer"""

    class Meta:
        model = Hotel
        fields = ('name', )
