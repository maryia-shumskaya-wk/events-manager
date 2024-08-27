from rest_framework import mixins, permissions, viewsets

from users.models import User
from users.serializers import UserSerializer


class UserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ViewSet for user registration"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
