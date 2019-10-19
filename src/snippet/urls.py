from rest_framework.routers import DefaultRouter

from .views import PastesViewset

app_name = 'snippet'

# create router for app viewset and return is as default urlpatterns
router = DefaultRouter()
router.register('pastes', PastesViewset, base_name='pastes')

urlpatterns = router.urls
