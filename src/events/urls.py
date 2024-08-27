from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet  # Adjust according to your application structure

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # Includes event management and participation endpoints
]
