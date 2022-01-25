from rest_framework.exceptions import MethodNotAllowed

from werewolf.models.game import Game


class GameViewGeneric(object):

    def dispatch(self, request, game_id):
        try:
            self.game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            raise MethodNotAllowed()

        return super().dispatch(request, game_id)
