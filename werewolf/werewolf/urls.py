from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from werewolf.views.games import MyGames, GameManagement
from werewolf.views.play import VoteView


me_router = DefaultRouter()
me_router.register(r'me/game', MyGames, basename='my-games')
me_router.register(r'game', GameManagement, basename='game-management')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/<game_id>/vote', VoteView.as_view(), name="game-vote")

] + me_router.urls
