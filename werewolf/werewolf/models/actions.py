from django.db import models

from .game import Round, Player


class SelectAction(models.Model):
    round = models.ForeignKey(to=Round, on_delete=models.CASCADE)
    who = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')
    whom = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True


class Elect(SelectAction):
    """
        Villager action to elect the mayor
    """
    permission = 'Game.can_elect'


class Vote(SelectAction):
    """
        Actions to vote against someone, and kill it at the end of the day
    """
    permission = 'Game.can_vote'


class Murder(SelectAction):
    """
       Werewolf actions to kill someone
    """
    permission = 'Game.can_murder'


class Predict(SelectAction):
    """
       Seer actions to predict the character of someone
    """
    permission = 'Game.can_predict'


class Link(SelectAction):
    """
        Cupidon action which link to player, to death
    """
    lover = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')
    permission = 'Game.can_link'


class Save(SelectAction):
    """
        Witch action to use potion to save someone
    """
    permission = 'Game.can_save'


class Poison(SelectAction):
    """
        Witch action to use potion to kill someone
    """
    permission = 'Game.can_poison'

# TODO Amoureux ? Post-Kill ?
# TODO Chasseur ? Post-Kill ?
