from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile as UserProfile
from .serializers import RegisterSerializer, UserProfileSerializer


User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = IsAuthenticated,
    allowed_methods = 'GET',

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserProfile(RetrieveAPIView, UpdateAPIView):
    queryset = UserProfile.objects.active()
    serializer_class = UserProfileSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.profile.pk)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
