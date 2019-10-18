from rest_framework.routers import DefaultRouter

from .views import PastesViewset

app_name = 'snippet'

router = DefaultRouter()
router.register('pastes', PastesViewset, base_name='pastes')

urlpatterns = router.urls
