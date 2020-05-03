from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin

from werewolf.views.generics import GameMixin
from werewolf.models.game import Game, Player
from werewolf.forms import StartGameForm
from werewolf.core.game import start_game


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['games'] = Game.objects.filter(owner=self.request.user)
        return context


class NewGame(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['name']
    template_name = 'new_game.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.save()
        assign_perm('change_game', self.request.user, form.instance)
        return super().form_valid(form)


class GameView(DetailView):
    model = Game
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.filter(game=context['game']).all()
        context['me'] = Player.objects.get(Q(owner=self.request.user) & Q(game=context['game']))
        return context


class JoinGame(LoginRequiredMixin, GameMixin, CreateView):
    model = Player
    fields = []
    template_name = 'join_game.html'
    success_url = '/'

    def form_valid(self, form):

        if self.game.status != Game.NOT_LAUNCHED:
            return HttpResponseNotAllowed('Game is already launched')

        form.instance.owner = self.request.user
        form.instance.game = self.game
        return super().form_valid(form)


class StartGame(GameMixin, LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'start_game.html'
    form_class = StartGameForm
    permission_required = 'change_game'

    def form_valid(self, form):

        if self.game.status != Game.NOT_LAUNCHED:
            return HttpResponseNotAllowed('Game is already launched')

        start_game(self.game, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game', args=(self.game.pk, ))
