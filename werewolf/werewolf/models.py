from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    @property
    def status(self):
        if self.end_date:
            return 'DONE'
        if self.start_date:
            return 'IN PROGRESS'
        return 'NOT LAUNCHED'
