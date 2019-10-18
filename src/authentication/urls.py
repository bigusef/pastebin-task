from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LogoutView,
    UserProfileView,
    StatisticsViewset,
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

router = DefaultRouter()
router.register('statistics', StatisticsViewset, base_name='statistics')
urlpatterns.extend(router.urls)
