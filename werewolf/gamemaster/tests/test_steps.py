import pytest
from django.urls import reverse

from gamemaster.models import NextStep


@pytest.mark.django_db
def test_stepconfig_exist_in_game(logged_client, game):
    assert game.stepsconfig


@pytest.mark.django_db
def test_round_from_started_game(logged_client, game):
    url = reverse('start-game', args=(game.pk, ))
    logged_client.post(url)

    next_step = NextStep.objects.get(game=game)
    assert next_step.step == NextStep.RESOLUTION
