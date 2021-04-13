import logging

from core.views import ManySerialziersView
from hotels.models import Hotel
from hotels.serializers import CreateHotelSerializer, HotelSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

logger = logging.getLogger(__name__)


class HotelView(ManySerialziersView, ModelViewSet):
    """List and create hotels."""

    serializer_class = {
        'list': HotelSerializer,
        'create': CreateHotelSerializer,
        'retrieve': HotelSerializer,
        'update': CreateHotelSerializer,
    }
    lookup_field = 'public_id'

    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        a = Hotel()
        # Get all items for cache
        values = a.get_many_values()
        # Serializers values
        serializer = self.get_serializer(values, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        a = Hotel()
        instance = a.get_value_by_id(
            kwargs.get(self.lookup_field)
        )
        if not instance:
            return Response(
                {'hotel': 'Value not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
