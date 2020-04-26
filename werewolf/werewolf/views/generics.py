from django.views.generic.detail import BaseDetailView

from django.http import Http404
from werewolf.models.game import Game


class GameMixin(object):
    model = Game
    pk_url_kwarg = 'game_id'

    def get_permission_object(self):
        return self.game

    def dispatch(self, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)

        try:
            self.game = Game.objects.filter(pk=pk).get()

        except Game.DoesNotExist:
            raise Http404("Game not found in query")
        return super().dispatch(*args, **kwargs)
