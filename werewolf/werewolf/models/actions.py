from django.db import models

from .game import Round, Player


class SelectAction(models.Model):
    round = models.ForeignKey(to=Round, on_delete=models.CASCADE)
    who = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')
    whom = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True
        unique_together = ("round", "who")


class Elect(SelectAction):
    """
        Villager action to elect the mayor
    """
    permission = 'Game.can_elect'


class Vote(SelectAction):
    """
        Actions to vote against someone, and kill it at the end of the day
    """
    permission = 'can_vote'

    def __str__(self):
        return f"Vote from \"{self.who.owner.username}\" against \"{self.whom.owner.username}\""


class Murder(SelectAction):
    """
       Werewolf actions to kill someone
    """
    permission = 'can_murder'


class Predict(SelectAction):
    """
       Seer actions to predict the character of someone
    """
    permission = 'can_predict'


class Link(SelectAction):
    """
        Cupidon action which link to player, to death
    """
    lover = models.ForeignKey(to=Player, on_delete=models.CASCADE, related_name='+')
    permission = 'can_link'


class Save(SelectAction):
    """
        Witch action to use potion to save someone
    """
    permission = 'can_save'


class Poison(SelectAction):
    """
        Witch action to use potion to kill someone
    """
    permission = 'can_poison'

# TODO Amoureux ? Post-Kill ?
# TODO Chasseur ? Post-Kill ?
