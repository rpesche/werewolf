from django.urls import reverse
import pytest

from werewolf.models.game import Player
from werewolf.models.actions import Vote


@pytest.fixture
def started_game(client, game_with_players):
    game = game_with_players
    url = reverse('start-game', args=(game.pk, ))
    client.login(username='test_user', password='test_password')
    client.post(url)
    game.refresh_from_db()
    yield game


@pytest.fixture
def dwight(game_with_players):
    yield Player.objects.get(owner__username='dwight')


@pytest.fixture
def mike(game_with_players):
    yield Player.objects.get(owner__username='mike')


@pytest.fixture
def pam(game_with_players):
    yield Player.objects.get(owner__username='pam')


@pytest.mark.django_db
def test_vote(client, started_game, mike, dwight):
    client.login(username='mike', password='mike_password')
    game = started_game

    url = reverse('action-vote', args=(game.pk, ))
    response = client.post(url, {'whom': dwight.pk})
    assert response.status_code == 200

    vote = Vote.objects.get(round=game.current_round, who=mike)
    assert vote.whom == dwight


@pytest.mark.django_db
def test_vote_me(client, started_game, mike):
    client.login(username='mike', password='mike_password')
    game = started_game

    url = reverse('action-vote', args=(game.pk, ))
    response = client.post(url, {'whom': mike.pk})
    assert response.status_code == 400


@pytest.mark.django_db
def test_only_one_vote(client, started_game, mike, dwight, pam):
    client.login(username='mike', password='mike_password')
    game = started_game

    url = reverse('action-vote', args=(game.pk, ))
    client.post(url, {'whom': dwight.pk})
    client.post(url, {'whom': pam.pk})

    vote = Vote.objects.get(round=game.current_round, who=mike)
    assert vote.whom == pam
