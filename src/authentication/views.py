from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_csv.renderers import CSVRenderer

from .models import Profile as UserProfile
from .serializers import RegisterSerializer, UserProfileSerializer, UserSerializer


# reference to defualt user model
User = get_user_model()


class RegisterView(CreateAPIView):
    """
    API view responsible for create new user account
    :return valid auth token key an user id and username
    """
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    API view responsible for logout current user
    """
    permission_classes = IsAuthenticated,
    allowed_methods = 'GET',

    def get(self, request, format=None):
        """
        ensure delete user token and return empty response with status 200
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserProfileView(RetrieveAPIView, UpdateAPIView):
    """
    API view with only two methods to handle user profile
    GET: to retrieve current login user profile model
    PUT: to update current login user profile model
    """
    queryset = UserProfile.objects.active()
    serializer_class = UserProfileSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        """
        override get_object method to only retrieve current login user model
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.profile.pk)
        self.check_object_permissions(self.request, obj)
        return obj


class StatisticsViewset(ReadOnlyModelViewSet):
    """
    reade only viewset responsible to return statistics about all users on system
    accessible by site admin users only (stuff user or super admin user)
    all API under this view set will return downloaded CSV file
    """
    queryset = UserProfile.objects.all()
    renderer_classes = CSVRenderer,
    permission_classes = IsAdminUser,
    serializer_class = UserSerializer
    pagination_class = None

    def get_renderer_context(self):
        """
        this methos responsible of returning file headers with specific order
        """
        context = super().get_renderer_context()
        header = (
            'username',
            'email',
            'full_name',
            'total_pastes',
            'available_pastes',
            'unavailable_pastes',
        )
        context['header'] = (header if 'fields' in self.request.GET else None)
        return context
