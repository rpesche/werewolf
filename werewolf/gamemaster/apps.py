from django.apps import AppConfig

from django.db.models.signals import post_save


class GamemasterConfig(AppConfig):
    name = 'gamemaster'

    def ready(self):
        from gamemaster.models import StepsConfig, NextStep  # noqa
        # This line is needed to setup `gamemaster` models in app
        # before importing it with `import on_new_game`
        # see : https://docs.djangoproject.com/en/3.0/ref/applications/#django.apps.AppConfig.ready

        from .signals import on_new_game
        post_save.connect(on_new_game, sender='werewolf.Game')
