from rest_framework import authentication, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Endpoint to create users"""

    serializer_class = UserSerializer


class ManageUserView(RetrieveUpdateAPIView):
    """Endpoint to manage authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Returns the authenticated user"""
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """Endpoint to create user authentication tokens"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
