from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView

from werewolf.models import Game


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
