from werewolf.views.generics import SelectActionMixin
from werewolf.models.actions import Vote, Murder


class VoteView(SelectActionMixin):
    model = Vote


class MurderView(SelectActionMixin):
    model = Murder
