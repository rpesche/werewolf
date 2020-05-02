import random

from django.utils import timezone
from guardian.shortcuts import assign_perm

from werewolf.models.game import Player, Round
from werewolf.models.character import Villager, Werewolf, Cupidon, Witch, Seer


def start_game(game, user):
    game.start_date = timezone.now()
    game.save()

    players = Player.objects.filter(game=game)
    for player in players:
        character = random.choice([Villager, Werewolf, Cupidon, Witch, Seer])
        set_player_character(player, character)
        set_up_permissions(player.owner, game, character)
    game.current_round = Round.objects.create(game=game, number=0)
    game.save()


def set_player_character(player, character_class):
    player.type = character_class.slug
    player.save()


def set_up_permissions(user, game, character):

    for permission in character.start_permissions:
        assign_perm(permission, user, game)
