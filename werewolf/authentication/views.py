from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'logout.html'
