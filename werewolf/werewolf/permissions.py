from rest_framework.permissions import BasePermission, DjangoObjectPermissions

from werewolf.models.game import Player


class GameManagementPermission(DjangoObjectPermissions):
    perms_map = {
        'POST': ['change_game'],
    }
    _ignore_model_permissions = True

    def has_permission(self, *args, **kwargs):
        return True


class PlayerPermission(BasePermission):

    def has_permission(self, request, view):
        if not Player.objects.filter(game=view.game, owner=request.user).exists():
            return False
        return True
