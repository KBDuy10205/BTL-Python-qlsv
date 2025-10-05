from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView,LogoutView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]