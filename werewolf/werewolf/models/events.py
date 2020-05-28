from django.db import models

from .game import Round, Player


class Event(models.Model):
    HANGED = 'HG'
    ELECTED = 'EL'
    MURDERED = 'MR'
    POISONED = 'PS'
    RESURRECTED = 'RS'
    LINKED = 'LK'

    YEAR_IN_SCHOOL_CHOICES = [
        (ELECTED, 'Elected as Mayor'),
        (HANGED, 'Hanged by villagers'),
        (MURDERED, 'Murdered by Werewolf'),
        (POISONED, 'Poisoned by Witch'),
        (RESURRECTED, 'Resurrected by Witch'),
        (LINKED, 'Linked as lovers by Cupidon'),
    ]

    round = models.ForeignKey(to=Round, on_delete=models.CASCADE)
    type = models.CharField()
    who = models.ForeignKey(to=Player, on_delete=models.CASCADE)
