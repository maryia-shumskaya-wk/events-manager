from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserView

router = DefaultRouter()
router.register(r"users", UserView, basename="user")

urlpatterns = [
    path("", include(router.urls)),  # Includes all user/token related URLs
]
