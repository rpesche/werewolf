from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from werewolf.models.game import Game, Player, Round
from werewolf.models.actions import Vote, Murder


class GameAdmin(GuardedModelAdmin):
    pass


class VoteAdmin(GuardedModelAdmin):
    pass


class MurderAdmin(GuardedModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Murder, MurderAdmin)
