from django.contrib import admin
from django.urls import include, path

from werewolf.views import HomeView, NewGame

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),

    path('', HomeView.as_view(), name='home'),
    path('werewolf/new', NewGame.as_view(), name='new-game'),
]
