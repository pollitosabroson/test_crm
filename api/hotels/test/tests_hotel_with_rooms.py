import logging

import pytest
from core.utils import parse_response_content
from django.urls import reverse
from hotels.test.factory import HotelFactory
from rest_framework import status

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('roiback.urls')
class TestListRooms:
    """Specific tests for list hotel."""

    @staticmethod
    def get_url(public_id):
        """Get url with params.
        Args:
            public_id(str): ID or code from hotel
        Return:
            Str: Url
        """

        return reverse(
            'hotels:list_create_rooms',
            kwargs={
                    'public_id': public_id
                }
        )

    @staticmethod
    def get_success_fixtures():
        """values list for cases where the endpoint
        have an answer success
        """

        hotel = HotelFactory.create_hotel_wiht_rooms(
            hotel_name=f'hotel test rooms'
        )
        return [
            {
                'params': {
                    'hotel_id': hotel.public_id
                }
            }
        ]

    def make_get_request(self, client, params=None, **kwargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or {}

        response = client.get(
            self.get_url(i_params.pop('hotel_id', None)),
            **headers
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        for fixtures in self.get_success_fixtures():
            response_content, response_status = self.make_get_request(
                client,
                params=fixtures['params']
            )
            assert status.HTTP_200_OK == response_status
