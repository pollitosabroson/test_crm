import logging

from django.core.cache import cache
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


class RedisConnection:
    """RedisConnection"""

    SEPARATOR = ':'
    TIMEOUT = None

    def __init__(self, *args, **kwargs):
        self.conn = get_redis_connection('default')
        self.cache = cache
        super(RedisConnection, self).__init__(*args, **kwargs)

    def _get_base_name(self):
        """Get value ."""
        if self._meta.verbose_name is None:
            raise AttributeError("verbose_name is none")
        return self._meta.verbose_name

    def _get_id(self, public_id, **kwargs):
        """Get public_id for redis.
        Args:
            public_id(str): Public public_id for object
        Return:
            str: public_id for redis
        """
        get_name = self._get_base_name()
        nested_id = kwargs.get('nested_id')
        if nested_id:
            return f'{get_name}{self.SEPARATOR}{nested_id}{self.SEPARATOR}{public_id}'  # NOQA
        return f'{get_name}{self.SEPARATOR}{public_id}'

    def get_value_by_id(self, public_id, **kwargs):
        """Get value from ID.
        Args:
            publid_id(str): public id
        Return
            Dict: dict from values to representation
        """
        value_id = self._get_id(public_id, **kwargs)
        obj = self._get_value(value_id)
        if obj is None:
            obj = self._set_value(public_id)

        return obj

    def get_many_values(self, public_id=None):
        """Get all values from cache.
        Args:
            public_id(str, Optional): public_id
        Return:
            List: list with all values
        """
        base_name = self._get_base_name()
        if public_id:
            values = self.cache.get_many(
                self.cache.keys(
                    f'{base_name}{self.SEPARATOR}{public_id}*'
                )
            )
        else:
            values = self.cache.get_many(cache.keys(f'{base_name}*'))
        return [
            v
            for k, v in values.items()
        ]

    def _get_value(self, public_id):
        """"Get value from redis.
        Args:
            public_id(str): public_id
        Return:
            Dict: dict from values to representation
        """
        return self.cache.get(public_id)

    def _set_value(self, public_id, **kwargs):
        """"Set value to redis.
        Args:
            public_id(str): public_id
        Return:
            Dict: dict from values to representation
        """
        try:
            obj = self.__class__.objects.get(public_id=public_id)
            value_id = self._get_id(public_id, **kwargs)
            json_value = obj.to_json()
            self.cache.set(
                value_id,
                json_value,
                self.TIMEOUT
            )
        except self.DoesNotExist:
            json_value = {}

        return json_value
