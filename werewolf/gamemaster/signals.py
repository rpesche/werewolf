from datetime import datetime, timedelta

from croniter import croniter

from gamemaster.models import StepsConfig, NextStep


def on_new_game(sender, instance, created, **kwargs):
    if created:
        instance.stepsconfig = StepsConfig.objects.create(game=instance)

        next_day = datetime.now() + timedelta(days=1)
        next_step_date = croniter(instance.stepsconfig.resolution, next_day).get_next(datetime)

        NextStep.objects.create(
            game=instance,
            step=NextStep.RESOLUTION,
            when=next_step_date,
        )
