import pytest
from django.urls import reverse

from werewolf.models.game import Game


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
