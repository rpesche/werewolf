from datetime import datetime
from collections import OrderedDict

from gamemaster.models import NextStep


def resolve_vote(game):
    # votes = Vote.objects.all(round, game)
    # hanged = votes.max()
    # new_event = Hanged(hanged)
    # return step(resolve)


def resolve_werewolf_murder(game):
    # murders = Murder.objects.all(round, game)
    # murdered = murders.max()
    # new_event = Murdered(murdered)
    # return step(resolve)
    pass


def resolve_witch_saving(game):
    # if poisoned = Poison(round, game):
    #    new_event(poisoned)
    # if res = Res(round, game):
    #    new_event(resurrected)
    # return step(resolve)
    pass


def resolve_round(game):
    # event = Events(round, game)
    # message(anybody, event)


STEPS = OrderedDict({
    NextStep.VOTE: resolve_vote,
    NextStep.MURDER: resolve_werewolf_murder,
    NextStep.WITCH: resolve_witch_saving,
    NextStep.RESOLUTION: resolve_round
})


def run():

    steps = NextStep.objects.filter(when__gt=datetime.now())
    for step in steps in steps:
        run_game_step(step.game, step)


def run_game_step(game, step):
    resolve_function = STEPS[step.step]

    resolve_function(game)
    # if is_anybody_win:
    #   close game
    # nextstep()
