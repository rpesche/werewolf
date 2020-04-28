from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin

from django.http import Http404
from werewolf.models.game import Game, Player


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


class SelectActionMixin(GameMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    fields = ["whom"]

    def get_required_permissions(self, request=None):
        return [self.model.permission]

    def form_valid(self, form):
        current_player = Player.objects.get(owner=self.request.user, game=self.game)

        if current_player == form.instance.whom:
            return JsonResponse({'error': 'Cannot vote against yourself'}, status=400)

        form.instance.who = current_player
        form.instance.round = self.game.current_round

        # Delete existing vote before adding it
        self.model.objects.filter(who=current_player, round=self.game.current_round).delete()
        form.instance.save()

        return JsonResponse({'pk': form.instance.pk})

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
