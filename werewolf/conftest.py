import pytest
from django.urls import reverse

from werewolf.models.game import Game


@pytest.fixture
def user(django_user_model):
    django_user_model.objects.create_user(username='test_user', password='test_password')


@pytest.fixture
def logged_client(user, client):
    client.login(username='test_user', password='test_password')
    yield client


@pytest.fixture
def game(logged_client):
    game_name = 'New Game'
    url = reverse('new-game')
    logged_client.post(url, data={'name': game_name})
    yield Game.objects.get(name=game_name)
