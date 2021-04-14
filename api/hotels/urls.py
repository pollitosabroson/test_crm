from django.urls import path, re_path
from rooms.views import RoomView

from . import views

app_name = 'hotels'
urlpatterns = [
    re_path(
        r'^(?P<public_id>[\w\-]+)/rooms/(?P<room_id>[\w\-]+)$',
        RoomView.as_view(
            {
                'get': 'retrieve',
                'patch': 'update'
            }
        ),
        name='single_hotel'
    ),
    re_path(
        r'^(?P<public_id>[\w\-]+)/rooms$',
        RoomView.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ),
        name='list_create_rooms'
    ),
    re_path(
        r'^(?P<public_id>[\w\-]+)$',
        views.HotelView.as_view(
            {
                'get': 'retrieve',
                'patch': 'update'
            }
        ),
        name='single_hotel'
    ),
    path(
        '',
        views.HotelView.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ),
        name='create_list_hotel'
    ),
]
