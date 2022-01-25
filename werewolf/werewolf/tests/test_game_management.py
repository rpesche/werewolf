import random
from http import HTTPStatus

import pytest
from django.urls import reverse
from guardian.shortcuts import get_perms
from rest_framework.test import APIClient
from freezegun import freeze_time

from werewolf.models.game import Game, Player
from werewolf.tests.factories import GameFactory, GameWithPlayers, PlayerFactory
from authentication.tests.factories import UserFactory


class TestListMyGame:

    @freeze_time("2012-01-14")
    def test_as_owner(self, db):
        me = UserFactory()
        GameFactory(owner=me)

        url = reverse('my-games-list')
        client = APIClient()
        client.force_authenticate(user=me)

        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                'owner': me.email,
                'name': 'My Game',
                'creation_date': '2012-01-14T00:00:00Z',
                'start_date': None,
                'end_date': None
            }
        ]

    @freeze_time("2012-01-14")
    def test_as_player(self, db):
        admin = UserFactory(username="admin")
        me = UserFactory(username="me")
        GameFactory(owner=admin, players=[me])

        url = reverse('my-games-list')
        client = APIClient()
        client.force_authenticate(user=me)

        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                'owner': 'admin@test.com',
                'name': 'My Game',
                'creation_date': '2012-01-14T00:00:00Z',
                'start_date': None,
                'end_date': None
            }
        ]

    def test_as_owner_and_player(self, db):
        me = UserFactory(username="me")
        GameFactory(owner=me, players=[me])

        url = reverse('my-games-list')
        client = APIClient()
        client.force_authenticate(user=me)

        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 1

    def test_no_games(self, db):
        admin = UserFactory(username="admin")
        GameFactory(owner=admin)

        url = reverse('my-games-list')
        client = APIClient()
        client.force_authenticate(user=UserFactory())

        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    def test_as_anonymous(self, db):
        admin = UserFactory(username="admin")
        GameFactory(owner=admin)

        url = reverse('my-games-list')
        client = APIClient()

        response = client.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestCreateGame:

    @freeze_time("2012-01-14")
    def test_create_game(self, db):
        me = UserFactory()
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-list')
        response = client.post(url, {'name': 'My Game'}, format='json')
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            'owner': me.email,
            'name': 'My Game',
            'creation_date': '2012-01-14T00:00:00Z',
            'start_date': None,
            'end_date': None
        }

        game = Game.objects.first()
        assert game.owner == me
        assert game.name == 'My Game'
        game.status == Game.NOT_LAUNCHED
        assert me.has_perm('change_game', game)

    def test_without_name(self, db):
        me = UserFactory()
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-list')
        response = client.post(url)
        assert response.status_code == HTTPStatus.BAD_REQUEST


class TestStartGame:

    def test_start_game(self, db):
        me = UserFactory()
        game = GameFactory(owner=me)
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        response = client.post(url)

        assert response.status_code == HTTPStatus.CREATED
        game.refresh_from_db()
        assert game.status == Game.IN_PROGRESS

    def test_not_owner(self, db):
        owner = UserFactory(username="owner")
        me = UserFactory(username="me")
        game = GameFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        response = client.post(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        game.refresh_from_db()
        assert game.status == Game.NOT_LAUNCHED

    def test_game_already_started(self, db):
        me = UserFactory()
        game = GameFactory(owner=me, status=Game.IN_PROGRESS)
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        response = client.post(url)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        game.refresh_from_db()
        assert game.status == Game.IN_PROGRESS


class TestStartedGamePermission:

    def test_permissions_with_no_player(self, db):
        me = UserFactory()
        game = GameFactory(owner=me)
        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        client.post(url)
        assert Player.objects.count() == 0

    def test_permissions(self, db):
        random.seed(42)

        me = UserFactory()
        game = GameWithPlayers(owner=me)

        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        client.post(url)

        player_roles = [
            ('mike', 'HUMA', {'can_elect', 'can_vote'}),
            ('dwight', 'HUMA', {'can_elect', 'can_vote'}),
            ('jim', 'CUPD', {'can_elect', 'can_vote', 'can_link'}),
            ('pam', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
            ('angela', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
            ('ryan', 'WOLF', {'can_elect', 'can_vote', 'can_murder'}),
            ('kelly', 'HUMA', {'can_elect', 'can_vote'}),
        ]

        for username, type, perms in player_roles:
            player = Player.objects.get(owner__username=username)
            assert player.type == type
            assert not set(get_perms(player.owner, game)) ^ perms

    @pytest.mark.xfail(reason="Correct randomization is not actually managed character are assigned evently")
    def test_multiple_truc(self, db):
        random.seed(1)

        me = UserFactory()
        game = GameFactory(owner=me)

        PlayerFactory(game=game, owner__username="mike")
        PlayerFactory(game=game, owner__username="dwight")
        PlayerFactory(game=game, owner__username="jim")
        PlayerFactory(game=game, owner__username="pam")
        PlayerFactory(game=game, owner__username="angela")
        PlayerFactory(game=game, owner__username="ryan")
        PlayerFactory(game=game, owner__username="kelly")

        client = APIClient()
        client.force_authenticate(user=me)

        url = reverse('game-management-start', args=(game.id,))
        client.post(url)

        assert Player.objects.filter(type='WTCH').count() <= 1
