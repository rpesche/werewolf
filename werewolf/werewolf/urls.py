from django.contrib import admin
from django.urls import include, path


from werewolf.views.game import HomeView, NewGame, GameView, JoinGame, StartGame
from werewolf.views.play import VoteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),

    # Game
    path('', HomeView.as_view(), name='home'),
    path('werewolf/new', NewGame.as_view(), name='new-game'),
    path('werewolf/game/<pk>', GameView.as_view(), name='game'),
    path('werewolf/game/<game_id>/join', JoinGame.as_view(), name='join-game'),
    path('werewolf/game/<game_id>/start', StartGame.as_view(), name='start-game'),

    # Play
    path('werewolf/game/<game_id>/vote', VoteView.as_view(), name='action-vote'),
]
