from django.contrib import admin
from django.urls import include, path


from werewolf.views import HomeView, NewGame, GameView, JoinGame

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),

    path('', HomeView.as_view(), name='home'),
    path('werewolf/new', NewGame.as_view(), name='new-game'),
    path('werewolf/game/<pk>', GameView.as_view(), name='game'),
    path('werewolf/game/<game_id>/join', JoinGame.as_view(), name='join-game'),
]
