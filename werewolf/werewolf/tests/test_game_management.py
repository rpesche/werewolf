import random

import pytest
from django.urls import reverse
from guardian.shortcuts import get_perms

from werewolf.models.game import Game, Player


@pytest.mark.django_db
def test_get_form_start_game(logged_client, game):
    url = reverse('start-game', args=(game.pk, ))
    response = logged_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_game(game):
    assert game.status == Game.NOT_LAUNCHED


@pytest.mark.django_db
def test_start_game(logged_client, game):
    url = reverse('start-game', args=(game.pk, ))
    logged_client.post(url)

    game.refresh_from_db()
    assert game.status == Game.IN_PROGRESS


@pytest.mark.django_db
def test_permissions_after_started_game(game_with_players, client):
    random.seed(42)
    player_roles = [
        ('mike', 'HUMA', {'can_elect', 'can_vote'}),
        ('dwight', 'HUMA', {'can_elect', 'can_vote'}),
        ('jim', 'CUPD', {'can_elect', 'can_vote', 'can_link'}),
        ('pam', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
        ('angela', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
        ('ryan', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
        ('kelly', 'HUMA', {'can_elect', 'can_vote'}),
    ]

    game = game_with_players
    url = reverse('start-game', args=(game.pk, ))
    client.login(username='test_user', password='test_password')
    client.post(url)

    for username, type, perms in player_roles:
        player = Player.objects.get(owner__username=username)
        assert player.type == type, f'{username}'
        assert not set(get_perms(player.owner, game)) ^ perms


@pytest.mark.django_db
def test_start_game_another_user(game, client, django_user_model):

    USERNAME = 'other_user'
    PASSWORD = 'other_password'

    django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)
    client.login(username=USERNAME, password=PASSWORD)
    url = reverse('start-game', args=(game.pk, ))
    client.post(url)

    game.refresh_from_db()
    assert game.status == Game.NOT_LAUNCHED


@pytest.mark.django_db
def test_start_nonexistant_game(logged_client):

    url = reverse('start-game', args=(42, ))
    response = logged_client.post(url)
    assert response.status_code == 404


def test_start_already_started_game(logged_client, game):
    url = reverse('start-game', args=(game.pk, ))
    logged_client.post(url)

    response = logged_client.post(url)
    assert response.status_code == 405


@pytest.mark.django_db
@pytest.mark.xfail(reason="Correct randomization is not actually managed character are assigned evently")
def test_multiple_truc(game_with_players, client):
    random.seed(1)
    game = game_with_players
    url = reverse('start-game', args=(game.pk, ))
    client.login(username='test_user', password='test_password')
    client.post(url)

    assert Player.objects.filter(type='WTCH').count() <= 1
