import logging

from core.views import ManySerialziersView
from hotels.models import Hotel
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rooms.models import Room
from rooms.serializers import CreateRoomSerializer, RoomSerializer

logger = logging.getLogger(__name__)


class RoomView(ManySerialziersView, ModelViewSet):
    """List and create Rooms."""

    serializer_class = {
        'list': RoomSerializer,
        'create': CreateRoomSerializer,
        'retrieve': RoomSerializer,
        'update': CreateRoomSerializer,
    }
    lookup_field = 'public_id'

    queryset = Room.objects.all()

    @staticmethod
    def base_value_not_found(field):
        """base values from raise 404.
        Args:
            Args(field): name of field dont exists
        Exception:
            Raise: Not found
        """
        raise NotFound(
            {field: 'Value not found'},
        )

    def valid_hotel(self, hotel_id):
        """Valid if hotel exists.
        Args:
            hotel_id(str): Hotel Id
        Return:
            Dict: Dict with values from hotels
        Exception:
            Raise: Not found
        """
        hotel = Hotel()
        instance = hotel.get_value_by_id(
            hotel_id
        )
        if not instance:
            self.base_value_not_found(
                'hotel'
            )
        return instance

    def perform_create(self, serializer):
        """Override performance create."""
        hotel_id = self.kwargs.get('public_id')
        hotel = self.valid_hotel(hotel_id)
        data = serializer.save(
            hotel=hotel.get('id')
        )
        return data

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """  # NOQA
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        hotel_id = self.kwargs.get('public_id')
        self.valid_hotel(hotel_id)
        rooms = Room()
        values = rooms.get_many_values(
            self.kwargs.get('public_id')
        )
        return values

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        hotel_id = self.kwargs.get('public_id')
        self.valid_hotel(hotel_id)
        room = Room()
        room_value = room.get_value_by_id(
            self.kwargs.get('room_id'),
            nested_id=hotel_id
        )
        if not room_value:
            self.base_value_not_found('room')
        return room_value
