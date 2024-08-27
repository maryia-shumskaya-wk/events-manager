from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.permissions import OwnsEventPermission
from events.filters import EventFilter
from events.models import Event
from events.serializers import EventSerializer
from events.services import attend_event, leave_event


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet to manage events created by the authenticated user and participation in events."""

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OwnsEventPermission]
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    @action(detail=True, methods=["put"], url_path="attend")
    def attend_event(self, request, pk=None):
        return attend_event(pk, request.user)

    @action(detail=True, methods=["put"], url_path="leave")
    def leave_event(self, request, pk=None):
        return leave_event(pk, request.user)
