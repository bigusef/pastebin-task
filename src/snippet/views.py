from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Pastes
from .serializers import PastesSerializer, AllwedUserSerializer
from .permissions import IsOwnedPastes, IsOwnedOrSharedPastes


class PastesViewset(ModelViewSet):
    model = Pastes
    queryset = Pastes.objects.all()
    serializer_class = PastesSerializer
    permission_classes = AllowAny,
    lookup_field = 'shortcode'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'auth_user': self.request.user
        })
        return context

    def list(self, request, *args, **kwargs):
        self.queryset = Pastes.objects.filter(privacy=Pastes.PUBLIC)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.privacy == Pastes.PRIVATE:
            self.permission_classes = IsOwnedPastes,
        elif instance.privacy == Pastes.SHARED:
            self.permission_classes = IsOwnedOrSharedPastes,
        else:
            self.permission_classes = AllowAny,
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.permission_classes = IsOwnedPastes,
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = IsOwnedPastes,
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = IsOwnedPastes,
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='my-pastes',
        url_name='my_pastes'
    )
    def auth_pastes(self, request, *args, **kwargs):
        owned = Pastes.objects.filter(author__user=self.request.user)
        shared = Pastes.objects.filter(allowed_user__user=self.request.user)
        self.queryset = owned.union(shared)
        return super().list(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['put'],
        permission_classes=[IsOwnedPastes, IsAuthenticated],
        url_path='shared-member',
        url_name='shared-member'
    )
    def edit_shared_member(self, request, shortcode, *args, **kwargs):
        serializer = AllwedUserSerializer(data=request.data)
        instance = self.get_object()
        if serializer.is_valid() and instance.privacy == Pastes.SHARED:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
