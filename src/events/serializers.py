from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for maintaining the operations connected to events"""

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        read_only_fields = ["created_at"]
        exclude = ["attendees"]
