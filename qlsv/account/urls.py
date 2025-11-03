from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView,LogoutView ,RefreshTokenView,ChangePasswordView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/',RefreshTokenView.as_view(), name='refresh_token'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]