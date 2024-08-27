import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


@pytest.mark.django_db
class TestUserTokenViewSet:
    def test_create_user(self, api_client, user_data):
        response = api_client.post(reverse("user-list"), user_data)
        assert response.status_code == status.HTTP_201_CREATED

        user_ = User.objects.get(email=user_data["email"])
        assert user_.first_name == user_data["first_name"]
        assert user_.last_name == user_data["last_name"]
        assert user_.check_password(user_data["password"])

    def test_create_user_duplicate_email(self, api_client, user_data):
        api_client.post(reverse("user-list"), user_data)
        response = api_client.post(reverse("user-list"), user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_tokens(self, api_client, login_data):
        response = api_client.post(reverse("token_obtain_pair"), login_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_refresh_token(self, api_client, login_data):
        obtain_response = api_client.post(reverse("token_obtain_pair"), login_data)
        access_token = obtain_response.data["access"]
        refresh_token = obtain_response.data["refresh"]

        refresh_url = reverse("token_refresh")
        refresh_data = {"refresh": refresh_token}

        refresh_response = api_client.post(refresh_url, refresh_data)
        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data
        assert refresh_response.data["access"] != access_token
