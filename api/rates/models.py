from core.models import PublicIdModel, TimeStampedModel
from django.db import models
from django.utils.translation import gettext as _
from inventories.models import Inventory
from rooms.models import Room


class Rate(PublicIdModel, TimeStampedModel):

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('room'),
        related_name=_('rates')
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        default=0
    )
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('rate'),
        related_name=_('rates')
    )

    class Meta:
        verbose_name = "rate"
        verbose_name_plural = "rates"

    def __str__(self):
        return self.name
