from django.contrib import admin
from werewolf.models.game import Game, Player


@admin.register(Game)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
