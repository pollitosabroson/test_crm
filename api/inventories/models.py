import logging

from core.managers import RedisConnection
from core.models import PublicIdModel, TimeStampedModel
from django.db import models

logger = logging.getLogger(__name__)


class Inventory(PublicIdModel, TimeStampedModel, RedisConnection):
    """Inventory models"""

    date = models.DateField()

    class Meta:
        verbose_name = "inventory"
        verbose_name_plural = "inventories"

    def __str__(self):
        return str(self.date)
