import logging

from inventories.serializers import CreateInventorySerializer
from rates.models import Rate
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class InventoryView(CreateAPIView):
    """Create an availability for a room."""

    serializer_class = CreateInventorySerializer


class FilterAvailabilityView(ListAPIView):
    """Filtering available rooms ."""

    serializer_class = CreateInventorySerializer

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
        rates = Rate.objects.filter(
            inventory__date__gte=self.kwargs.get('checkin'),
            inventory__date__lte=self.kwargs.get('checkout'),
            room__hotel__public_id=self.kwargs.get('hotel_id')
        ).values('room__public_id', 'price', "inventory__date")
        return rates

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        values = self.parse_values(queryset)
        return Response(values)

    @staticmethod
    def parse_values(values):
        """Convert values to representation.
        Args:
            values(List): List of values from bbdd
        Return:
            Dict: Values to representation
        """
        rates = {}
        rooms = {}
        for rate in values:
            if rate['room__public_id'] in rates.keys():
                rates[rate['room__public_id']].append(rate)
            else:
                rates[rate['room__public_id']] = [
                    rate
                ]
        for k, v in rates.items():
            rates = []
            base_rate = {}
            for values in v:
                if k in base_rate.keys():
                    base_rate[k]['total_price'] += values['price']
                    base_rate[k]['breakdown'].append(
                        {
                            str(values['inventory__date']): {
                                'price': values['price'],
                                'allotment': 1
                            }
                        }
                    )
                else:
                    base_rate[k] = {
                        'total_price': values['price'],
                        'breakdown': [
                            {
                                str(values['inventory__date']): {
                                    'price': values['price'],
                                    'allotment': 1
                                }
                            }
                        ]
                    }

            rooms.update(base_rate)

        rooms = {
            'rooms': [
                rooms
            ]
        }
        return rooms
