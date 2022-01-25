from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin

from werewolf.models.game import Game, Player
from werewolf.models.actions import Vote
from werewolf.serializers import VoteSerializer
from werewolf.views.generics import GameViewGeneric
from werewolf.permissions import PlayerPermission


class VoteView(GameViewGeneric, UpdateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [PlayerPermission]

    def get_object(self):
        player = Player.objects.get(owner=self.request.user, game=self.game)

        try:
            return Vote.objects.get(
                round=self.game.current_round,
                who=player
            )
        except Vote.DoesNotExist:
            return Vote(
                round=self.game.current_round,
                who=player
            )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["game"] = self.game
        context["me"] = Player.objects.get(owner=self.request.user, game=self.game)
        return context

    def post(self, request, game_id):
        return self.update(request, game_id)
