from werewolf.views.generics import SelectActionMixin
from werewolf.models.actions import Vote


class VoteView(SelectActionMixin):
    model = Vote
