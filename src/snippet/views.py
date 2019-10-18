from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Pastes
from .serializers import PastesSerializer


class PastesViewset(ModelViewSet):
    model = Pastes
    queryset = Pastes.objects.all()
    serializer_class = PastesSerializer
    permission_classes = AllowAny
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
