from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Game(models.Model):

    DONE = 'DONE'
    IN_PROGRESS = 'IN_PROGRESS'
    NOT_LAUNCHED = 'NOT_LAUNCHED'

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    @property
    def status(self):
        if self.end_date:
            return self.DONE
        if self.start_date:
            return self.IN_PROGRESS
        return self.NOT_LAUNCHED

    def start(self):
        self.start_date = timezone.now()


class Player(models.Model):
    HUMAN = 'HUMA'
    WEREWOLF = 'WOLF'
    UNDEFINED = 'NONE'

    PLAYER_CATEGORY = [
        (UNDEFINED, 'Undefined'),
        (HUMAN, 'Human'),
        (WEREWOLF, 'Werewolf'),
    ]

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=4,
        choices=PLAYER_CATEGORY,
        default=UNDEFINED,
    )

    class Meta:
        unique_together = ('game', 'owner',)
