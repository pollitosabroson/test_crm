import logging

from core.managers import RedisConnection
from core.models import PublicIdModel, TimeStampedModel
from django.db import models

logger = logging.getLogger(__name__)


class Hotel(PublicIdModel, TimeStampedModel, RedisConnection):
    """Hotel Model."""

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "hotel"
        verbose_name_plural = "hotels"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save for save values un caches"""
        super(Hotel, self).save(*args, **kwargs)
        self._set_value(self.public_id)

    def to_json(self):
        """conver Hotel value to json for redis.
        Return:
            Dict: Dict with representation value for redis.
        """
        return {
            "id": self.id,
            "created_date": str(self.created_date),
            "last_modified": str(self.last_modified),
            "name": self.name,
            "public_id": self.public_id,
        }
