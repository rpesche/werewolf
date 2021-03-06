from django.contrib.auth import views as auth_views
from django.urls import path

from authentication.views import RegisterView, LogoutView

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(template_name='login.html'), name='register'),
]
