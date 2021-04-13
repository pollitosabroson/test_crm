import logging

from core.managers import RedisConnection
from core.models import PublicIdModel, TimeStampedModel
from django.db import models
from django.utils.translation import gettext as _
from hotels.models import Hotel

logger = logging.getLogger(__name__)


class Room(PublicIdModel, TimeStampedModel, RedisConnection):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('hotel'),
        related_name=_('hotel')
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "room"
        verbose_name_plural = "rooms"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save for save values un caches"""
        super(Room, self).save(*args, **kwargs)
        self._set_value(self.public_id, nested_id=self.hotel.public_id)

    def to_json(self):
        """conver rooms value to json for redis.
        Return:
            Dict: Dict with representation value for redis.
        """
        return {
            "id": self.id,
            "created_date": str(self.created_date),
            "last_modified": str(self.last_modified),
            "name": self.name,
            "public_id": self.public_id,
            "hotel": self.hotel.public_id
        }
