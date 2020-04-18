import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, FormView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.http import HttpResponseNotAllowed

from werewolf.models import Game, Player
from werewolf.forms import StartGameForm


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
        return super().form_valid(form)


class GameView(DetailView):
    model = Game
    template_name = 'game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.filter(game=context['game']).all()
        return context


class JoinGame(LoginRequiredMixin, CreateView):
    model = Player
    fields = []
    template_name = 'join_game.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['game_id'])

        if self.game.status != Game.NOT_LAUNCHED:
            return HttpResponseNotAllowed('Game is already launched')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.game = self.game
        return super().form_valid(form)


class StartGame(FormView):
    template_name = 'start_game.html'
    form_class = StartGameForm

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['game_id'])

        if self.game.status != Game.NOT_LAUNCHED:
            return HttpResponseNotAllowed('Game is already launched')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.game.start_date = datetime.date.today()
        self.game.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game', args=(self.game.pk, ))
