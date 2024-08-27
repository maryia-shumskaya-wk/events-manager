import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from events.models import Event


@pytest.mark.django_db
class TestEventViewSet:
    def test_create_event_by_au_user(self, au_client, event_data):
        response = au_client.post(reverse("event-list"), event_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
        assert Event.objects.get().title == "Test Event"

    def test_create_event_by_not_au_user(self, client, event_data):
        response = client.post(reverse("event-list"), event_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_event_as_owner(self, au_client, event):
        url = reverse("event-detail", kwargs={"pk": event.pk})
        updated_data = {
            "title": "Summer Party",
            "description": "Music & Food",
            "end_date": "2024-08-31T23:00:00Z",
        }

        response = au_client.patch(url, updated_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        event.refresh_from_db()
        assert event.title == "Summer Party"
        assert event.end_date != "2024-08-31T17:00:00Z"

    def test_update_event_as_non_owner(self, user2, event):
        client = APIClient()
        client.force_authenticate(user=user2)

        url = reverse("event-detail", kwargs={"pk": event.pk})
        updated_data = {
            "title": "Summer Party",
            "description": "Music & Food",
            "end_date": "2024-08-31T23:00:00Z",
        }

        response = client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        event.refresh_from_db()
        assert event.title == "Test Event"

    def test_user_can_attend_event(self, au_client, event, user):
        url = reverse("event-attend-event", kwargs={"pk": event.pk})
        response = au_client.put(url)
        assert response.status_code == status.HTTP_200_OK
        assert event.attendees.filter(pk=user.pk).exists()

    def test_user_cannot_attend_event_twice(self, au_client, event, user):
        url = reverse("event-attend-event", kwargs={"pk": event.pk})
        response = au_client.put(url)

        assert response.status_code == status.HTTP_200_OK
        assert event.attendees.filter(pk=user.pk).exists()

        url = reverse("event-attend-event", kwargs={"pk": event.pk})
        response = au_client.put(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert f"You already attended {event.title}" in response.data["detail"]

    def test_user_cannot_attend_event_after_start(self, au_client, user, past_event):
        url = reverse("event-attend-event", kwargs={"pk": past_event.pk})
        response = au_client.put(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
