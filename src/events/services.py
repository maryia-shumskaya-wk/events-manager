from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from events.models import Event


def attend_event(pk, user):
    event = get_object_or_404(Event, pk=pk, start_date__gt=timezone.now())

    if user in list(event.attendees.all()):
        return Response(
            {
                "detail": f"You already attended {event.title}. See you at {event.start_date}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if event.attendees.count() >= event.max_attendees > 0:
        return Response(
            {"detail": "Cannot attend this event; attendee limit reached."},
            status=status.HTTP_403_FORBIDDEN,
        )

    event.attendees.add(user)
    return Response(
        {
            "message": f"You're now attending event {event.title}. "
            f"Event will start at {event.start_date}"
        },
        status=status.HTTP_200_OK,
    )


def leave_event(pk, user):
    event = get_object_or_404(Event, pk=pk, start_date__gt=timezone.now())

    if user not in list(event.attendees.all()):
        return Response(
            {
                "detail": f"You already left {event.title}. See you at {event.start_date}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    event.attendees.remove(user)
    return Response(
        {"message": f"You're no longer attending {event.title} event"},
        status=status.HTTP_200_OK,
    )
