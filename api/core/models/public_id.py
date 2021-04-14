# -*- coding: utf-8 -*-
import random
import string

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

BASE = string.digits + string.ascii_letters


def calculate_random_id(default_name):
    """Calculate random id for new object.
    Args:
        default_name: Default value to start the code with
    Return:
        Str: String wiht randmon values
    """
    l_name = settings.LONG_PUBLIC_ID - len(default_name)
    return default_name + '_' + ''.join(
        [
            random.choice(BASE)
            for i in range(l_name - 1)
        ]
    )


class PublicIdModel(models.Model):
    """
    Abstract model that defines the 'public_id' field which is auto populated
    by a ramdom combination of items iside the digits, lowercase and
    upercase letters.
    """

    public_name = None
    public_id = models.CharField(
        unique=True,
        db_index=True,
        editable=False,
        max_length=settings.LONG_PUBLIC_ID,
        verbose_name=_('public_id')
    )

    class Meta:
        abstract = True


@receiver(pre_save)
def populate_public_id(sender, instance, **kwargs):
    if issubclass(sender, PublicIdModel):
        while not instance.public_id:
            candidate = calculate_random_id(
                instance._meta.verbose_name
            )
            try:
                sender.objects.get(public_id=candidate)

            except sender.DoesNotExist:
                instance.public_id = candidate
