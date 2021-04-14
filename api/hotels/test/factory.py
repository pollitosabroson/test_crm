import logging

from hotels.models import Hotel
from rooms.models import Room

logger = logging.getLogger(__name__)


class Roomfactory:
    """Class in charge of creating room objects."""

    @staticmethod
    def _get_room(name, hotel, **kwargs):
        """
        Return instance room
        """
        room, _ = Room.objects.get_or_create(
            name=name,
            hotel=hotel
        )
        return room

    @classmethod
    def get_room(cls, name, hotel, **kwargs):
        """Get single room.
        Args:
            name(str): name of room
            hotel(Instance): hotel
        Return:
            Instance: Instance of room
        """
        room = cls._get_room(
            name=name,
            hotel=hotel
        )
        return room


class HotelFactory:
    """Class in charge of creating Hotel objects."""

    DEFUALT_ROOMS = 5

    @staticmethod
    def _get_hotel(name, **kwargs):
        """
        Return instance hotel
        """
        hotel, _ = Hotel.objects.get_or_create(
            name=name
        )
        hotel.save()
        return hotel

    @classmethod
    def get_hotel(cls, **kwargs):
        return cls._get_hotel(
            **kwargs
        )

    @classmethod
    def create_hotel_wiht_rooms(cls, **kwargs):
        if not kwargs.get('hotel'):
            hotel = cls._get_hotel(
                name=kwargs.get('hotel_name', 'hotel_test')
            )
        for value in range(0, kwargs.get('total_rooms', cls.DEFUALT_ROOMS)):  # NOQA
            Roomfactory.get_room(
                name=f'room name {value}',
                hotel=hotel
            )
        return hotel
