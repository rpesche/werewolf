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


@pytest.fixture
def players(django_user_model):
    players_names = [
        "mike",
        "dwight",
        "jim",
        "pam",
        "angela",
        "ryan",
        "kelly"
    ]

    users = []
    for player_name in players_names:
        username = player_name
        password = f'{player_name}_password'
        new_user = django_user_model.objects.create_user(username=username, password=password)
        users.append(new_user)
    yield users


@pytest.fixture
def game_with_players(client, game, players):

    url = reverse('join-game', args=(game.pk, ))
    for player in players:
        username = player.username
        password = f'{username}_password'
        client.login(username=username, password=password)
        client.post(url)
    yield game
