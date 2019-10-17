from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    RegisterView,
    LogoutView,
    UserProfile,
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
]
