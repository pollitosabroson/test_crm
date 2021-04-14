import json
import logging
import random

import pytest
from core.utils import parse_response_content
from django.urls import reverse
from hotels.test.factory import HotelFactory
from rest_framework import status

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('roiback.urls')
class TestCreateHotels:
    """Specific tests for create Room."""

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
        names = ('Johnson', 'Smith', 'Williams')

        hotel = TestCreateHotels.create_hotel()
        return [
            {
                'params': {
                    'name': random.choice(names),
                    'hotel_id': hotel.public_id
                }
            },
            {
                'params': {
                    'name': random.choice(names),
                    'hotel_id': hotel.public_id
                }
            },
            {
                'params': {
                    'name': random.choice(names),
                    'hotel_id': hotel.public_id
                }
            },
            {
                'params': {
                    'name': random.choice(names),
                    'hotel_id': hotel.public_id
                }
            },
        ]

    @staticmethod
    def create_hotel():
        """Create hotel for new room.
        Return:
            Instance: Instance for hotel
        """
        return HotelFactory.get_hotel(name='hote room')

    @staticmethod
    def get_bad_request_fixtures():
        """User list for cases where the endpoint
        have a fail answer
        """
        return [
            {
                'params': {}
            },
            {},
        ]

    def make_post_request(self, client, params=None, **kwargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or {}
        body = {}
        body.update(**i_params)
        body = json.dumps(body)
        response = client.post(
            self.get_url(i_params.pop('hotel_id', None)),
            body,
            **headers
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        for fixtures in self.get_success_fixtures():
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures['params']
            )
            assert status.HTTP_201_CREATED == response_status
            assert response_content['name'] == fixtures['params']['name']

    def test_bad_request(self, client):
        """Test to validate that a user cannot be edited."""
        for fixtures in self.get_bad_request_fixtures():
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_400_BAD_REQUEST == response_status
