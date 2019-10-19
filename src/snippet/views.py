from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Pastes
from .serializers import PastesSerializer, AllwedUserSerializer
from .permissions import IsOwnedPastes, IsOwnedOrSharedPastes


class PastesViewset(ModelViewSet):
    model = Pastes
    queryset = Pastes.objects.available()
    serializer_class = PastesSerializer
    permission_classes = AllowAny,
    lookup_field = 'shortcode'

    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        lte = self.request.query_params.get('lte', None)
        gte = self.request.query_params.get('gte', None)

        if date:
            self.queryset = self.queryset.filter(created__date=parse_date(date))
        if lte:
            self.queryset = self.queryset.filter(created__date__lte=parse_date(lte))
        if gte:
            self.queryset = self.queryset.filter(created__date__gte=parse_date(gte))
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'auth_user': self.request.user
        })
        return context

    def list(self, request, *args, **kwargs):
        self.queryset = Pastes.objects.available(privacy=Pastes.PUBLIC)
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
        self.queryset = Pastes.objects.available(
            Q(author__user=self.request.user) | Q(allowed_user__user=self.request.user)
        )
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

    @action(
        detail=False,
        methods=['get'],
        url_path='search',
        url_name='search'
    )
    def pastes_search(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            self.queryset = Pastes.objects.available(
                Q(author__user=user) | Q(allowed_user__user=user) | Q(privacy=Pastes.PUBLIC)
            )
        else:
            self.queryset = Pastes.objects.available(privacy=Pastes.PUBLIC)
        return super().list(request, *args, **kwargs)
