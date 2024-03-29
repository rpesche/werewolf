from django.db import models
from django.conf import settings

from .character import RegisteredCharacters, Unknown


class Round(models.Model):
    game = models.ForeignKey(to='Game', on_delete=models.CASCADE, related_name='rounds')
    number = models.IntegerField()


class Game(models.Model):

    DONE = 'DONE'
    IN_PROGRESS = 'IN_PROGRESS'
    NOT_LAUNCHED = 'NOT_LAUNCHED'

    owner = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    current_round = models.ForeignKey(to=Round, on_delete=models.SET_NULL, default=None, null=True, related_name='+')

    @property
    def status(self):
        if self.end_date:
            return self.DONE
        if self.start_date:
            return self.IN_PROGRESS
        return self.NOT_LAUNCHED

    def __str__(self):
        return f"\"{self.name}\" game"

    class Meta:
        permissions = (
            ('can_elect', 'Elect a player to be mayor'),
            ('can_vote', 'Vote against a player to be hanged'),
            ('can_murder', 'Werewolf vote to kill someone'),
            ('can_predict', 'Seer hability to predict someone character'),
            ('can_link', 'Cupidon hability to link to player to death'),
            ('can_save', 'Witch hability to save someone'),
            ('can_poison', 'Witch hability to kill someone'),
        )


class Player(models.Model):
    owner = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=4,
        choices=[(slug, name) for slug, name, _ in RegisteredCharacters.registered_characters],
        default=Unknown.slug,
    )

    class Meta:
        unique_together = ('game', 'owner',)

    @property
    def vote(self):
        from .actions import Vote

        try:
            return Vote.objects.get(models.Q(round=self.game.current_round) & models.Q(who=self))
        except Vote.DoesNotExist:
            return None

    @property
    def murder(self):
        from .actions import Murder

        try:
            return Murder.objects.get(models.Q(round=self.game.current_round) & models.Q(who=self))
        except Murder.DoesNotExist:
            return None

    def __str__(self):
        return f"Player {self.owner.username} on {self.game.name} as {self.type}"
