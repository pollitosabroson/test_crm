from datetime import datetime

from django.urls import path, register_converter

from . import views


class DateConverter:
    """Parse date for urls"""

    regex = '\d{4}-\d{2}-\d{2}'  # NOQA

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')


urlpatterns = [
    path(
        '<str:hotel_id>/<yyyy:checkin>/<yyyy:checkout>',
        views.FilterAvailabilityView.as_view(),
        name='date'
    ),
    path(
        '',
        views.InventoryView.as_view(),
        name='create_list_inventory'
    ),
]
