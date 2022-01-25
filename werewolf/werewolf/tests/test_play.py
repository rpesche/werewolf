import random
from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from werewolf.tests.factories import StartedGame
from werewolf.models.actions import Vote


class TestVote:

    def test_vote(self, db):
        random.seed(42)

        game = StartedGame()
        player = game.player_set.first()  # Mike
        whom = game.player_set.last()

        url = reverse('game-vote', args=(game.pk,))

        data = {
            "whom": whom.pk
        }

        client = APIClient()
        client.force_authenticate(user=player.owner)
        response = client.post(url, data=data, format='json')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "round": 1,
            "who": player.pk,
            "whom": whom.pk,
        }
        Vote.objects.get(who=player, whom=whom)

    def test_vote_me(self, db):
        random.seed(42)

        game = StartedGame()
        me = game.player_set.first()  # Mike

        url = reverse('game-vote', args=(game.pk,))
        data = {
            "whom": me.pk
        }

        client = APIClient()
        client.force_authenticate(user=me.owner)
        response = client.post(url, data=data, format='json')
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert not Vote.objects.all().exists()

    def test_only_one_vote(self, db):
        random.seed(42)

        game = StartedGame()
        me = game.player_set.first()
        seconde_vote = game.player_set.all()[1]
        first_vote = game.player_set.all()[2]

        client = APIClient()
        client.force_authenticate(user=me.owner)

        url = reverse('game-vote', args=(game.pk,))
        client.post(url, data={"whom": first_vote.pk}, format='json')
        client.post(url, data={"whom": seconde_vote.pk}, format='json')

        vote = Vote.objects.first()
        assert Vote.objects.count() == 1
        assert vote.whom == seconde_vote
        assert vote.who == me

    def test_not_on_the_game(self, db):
        random.seed(42)

        game = StartedGame()
        me = UserFactory()

        vote = game.player_set.all()[2]

        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-vote', args=(game.pk,))
        response = client.post(url, data={"whom": vote.pk}, format='json')
        assert response.status_code == HTTPStatus.FORBIDDEN

        assert not Vote.objects.all().exists()
