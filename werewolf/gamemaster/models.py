from django.db import models

from werewolf.models.game import Game


class StepsConfig(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    elect_date = models.CharField(max_length=32, default="0 18 * * *")  # Defaut vote at 18h
    murder_date = models.CharField(max_length=32, default="0 22 * * *")  # Murder à 22h
    wich_date = models.CharField(max_length=32, default="0 2 * * *")  # Wich poison/res until 2h
    resolution = models.CharField(max_length=32, default="0 6 * * *")  # Dead can act until 6h


class NextStep(models.Model):
    VOTE = 'VOTE'
    MURDER = 'MURDER'
    WITCH = 'WITCH'
    RESOLUTION = 'RESOL'

    STEPS = [
        (VOTE, 'Vote'),
        (MURDER, 'Murder'),
        (WITCH, 'Witch'),
        (RESOLUTION, 'Resolution'),
    ]

    step = models.CharField(max_length=6, choices=STEPS, default=VOTE)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    when = models.DateTimeField()
