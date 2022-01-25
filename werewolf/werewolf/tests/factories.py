from datetime import datetime

import factory
from guardian.shortcuts import assign_perm

from werewolf.models import Game, Player
from werewolf.core.game import start_game
from authentication.tests.factories import UserFactory


class PlayerFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Player


class GameFactory(factory.django.DjangoModelFactory):

    owner = factory.SubFactory(UserFactory)
    name = 'My Game'
    creation_date = datetime(2022, 1, 1, 12, 12)

    class Meta:
        model = Game

    @factory.post_generation
    def players(self, create, extracted):
        if not create or not extracted:
            return

        for user in extracted:
            PlayerFactory(owner=user, game=self)

    @factory.post_generation
    def set_owner_permission(self, create, extracted):
        assign_perm('change_game', self.owner, self)

    @factory.post_generation
    def status(self, create, extracted):
        if not create or not extracted:
            return

        if extracted == Game.IN_PROGRESS:
            start_game(self, self.owner)


class GameWithPlayers(GameFactory):

    mike = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="mike"
    )
    dwight = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="dwight"
    )
    jim = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="jim"
    )
    pam = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="pam"
    )
    angela = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="angela"
    )
    ryan = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="ryan"
    )
    kelly = factory.RelatedFactory(
        PlayerFactory,
        factory_related_name="game",
        owner__username="kelly"
    )


class StartedGame(GameWithPlayers):

    @factory.post_generation
    def start_game(self, create, extracted):

        if not create:
            return

        start_game(self, self.owner)
