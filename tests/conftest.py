import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from events.models import Event
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@gmail.com",
        password="strong_password_123",
        first_name="Jane",
        last_name="Doe",
    )


@pytest.fixture
def user2():
    return User.objects.create_user(
        email="testuser2@gmail.com",
        password="strong_password_123",
        first_name="John",
        last_name="Doe",
    )


@pytest.fixture
def create_user(api_client):
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "password123",
    }
    api_client.post(reverse("user-list"), user_data)
    return user_data


@pytest.fixture
def user_data():
    return {
        "email": "testuser2@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "strong_password_123",
    }


@pytest.fixture
def login_data(create_user):
    return {
        "email": create_user["email"],
        "password": create_user["password"],
    }


@pytest.fixture
def registration_data():
    return {
        "password": "strong_password_123",
        "email": "testuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def event(user):
    return Event.objects.create(
        title="Test Event",
        description="A test event.",
        start_date="2024-08-31T17:00:00Z",
        end_date="2024-08-31T22:00:00Z",
        created_by=user,
    )


@pytest.fixture
def au_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def event_data(user):
    return {
        "title": "Test Event",
        "description": "A test event.",
        "start_date": timezone.now() + timezone.timedelta(days=1),
        "end_date": timezone.now() + timezone.timedelta(days=2),
        "created_by": user,
    }


@pytest.fixture
def past_event(user):
    return Event.objects.create(
        title="Past Test Event",
        description="A finished test event",
        start_date="2024-08-01T17:00:00Z",
        end_date="2024-08-02T22:00:00Z",
        created_by=user,
    )
