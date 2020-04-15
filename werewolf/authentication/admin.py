from django.contrib import admin
from werewolf.models import Game


@admin.register(Game)
class AuthorAdmin(admin.ModelAdmin):
    pass
