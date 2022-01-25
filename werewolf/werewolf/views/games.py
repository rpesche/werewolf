from rest_framework import viewsets, mixins, decorators, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from guardian.shortcuts import assign_perm

from werewolf.models.game import Game, Player
from werewolf.serializers import GameSerializer
from werewolf.permissions import GameManagementPermission
from werewolf.core.game import start_game


class MyGames(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Game
    serializer_class = GameSerializer

    def get_queryset(self):
        game_as_owner = Game.objects.filter(owner=self.request.user)
        game_as_player_id = Player.objects.filter(owner=self.request.user).values_list("game", flat=True)
        game_as_player = Game.objects.filter(pk__in=game_as_player_id)
        return (game_as_player | game_as_owner).distinct()


class GameManagement(viewsets.GenericViewSet, mixins.CreateModelMixin):

    model = Game
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    permission_classes = [GameManagementPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        assign_perm('change_game', self.request.user, serializer.instance)
        return serializer.instance

    @decorators.action(detail=True, methods=['post'])
    def start(self, request, pk):
        game = self.get_object()

        if game.status != Game.NOT_LAUNCHED:
            raise ParseError('Game is already launched')

        start_game(game, self.request.user)
        return Response(status=status.HTTP_201_CREATED)
