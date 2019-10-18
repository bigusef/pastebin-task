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


User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = IsAuthenticated,
    allowed_methods = 'GET',

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserProfileView(RetrieveAPIView, UpdateAPIView):
    queryset = UserProfile.objects.active()
    serializer_class = UserProfileSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.profile.pk)
        self.check_object_permissions(self.request, obj)
        return obj


class StatisticsViewset(ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    renderer_classes = CSVRenderer,
    permission_classes = IsAdminUser,
    serializer_class = UserSerializer
    pagination_class = None

    def get_renderer_context(self):
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
