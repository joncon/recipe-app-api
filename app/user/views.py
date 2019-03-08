from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    '''create a new user'''
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    '''create a new auth token for user'''

    serialzer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''manage the authenticated user'''
    serializer_class = UserSerializer
    # IMPORTANT!!! make sure you have the trailing ',' below
    authentication_classes = (authentication.TokenAuthentication,)
    # must be authenticated
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        '''retrieve and return auth user'''
        return self.request.user
