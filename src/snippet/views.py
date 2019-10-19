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
    """
    Pastes view set hold all API views for Pastes model
    """

    # viewset attribute
    model = Pastes
    queryset = Pastes.objects.available()
    serializer_class = PastesSerializer
    permission_classes = AllowAny,
    lookup_field = 'shortcode'  # make sure the lookup field is became shortcode not pk

    def get_queryset(self):
        """
        overrider get_queryset method to provide filter all pastes list with date by three ways
        - date get all pastes created on this date
        - lte get all pastes created less than or equal this date
        - gte get all pastes created less grate or equal this date

        :return call super method from parent class
        """
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
        """
        override context before passed to serializer class and add current login user
        :return updated context
        """
        context = super().get_serializer_context()
        context.update({
            'auth_user': self.request.user
        })
        return context

    def list(self, request, *args, **kwargs):
        """
        override list queryset and return just all public pastes
        :return call super method from parent class
        """
        self.queryset = Pastes.objects.available(privacy=Pastes.PUBLIC)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        decide retrive class permission based on instance privacy
        - privacy is public any one can see pastes
        - privacy is sheard only owner and shared member can see pastes
        - privacy is privet only owner can see pastes
        :return call super method from parent class
        """
        instance = self.get_object()
        if instance.privacy == Pastes.PRIVATE:
            self.permission_classes = IsOwnedPastes,
        elif instance.privacy == Pastes.SHARED:
            self.permission_classes = IsOwnedOrSharedPastes,
        else:
            self.permission_classes = AllowAny,
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        only owner of paste can edit it
        :return call super method from parent class
        """
        self.permission_classes = IsOwnedPastes,
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        only owner of paste can edit it
        :return call super method from parent class
        """
        self.permission_classes = IsOwnedPastes,
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        only owner of paste can delete it
        :return call super method from parent class
        """
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
        """
        this action will return all pastes for current login user
        :return call super list method from parent class
        """
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
        """
        this action is responsbile on edit shared member for specific pastes
        only owner of paste can edit this list
        :return response with status 201 is relation updated and 400 if not
        """
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
        """
        action to list all pastes based on user 
        if user is authenticated return all not expire public pastes and include his privet pastes and his shared pastes
        if user is anonymous user return all not expire public pastes
        :return call super list method from parent class
        """
        user = request.user
        if user.is_authenticated:
            self.queryset = Pastes.objects.available(
                Q(author__user=user) | Q(allowed_user__user=user) | Q(privacy=Pastes.PUBLIC)
            )
        else:
            self.queryset = Pastes.objects.available(privacy=Pastes.PUBLIC)
        return super().list(request, *args, **kwargs)
