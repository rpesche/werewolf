

class RegisteredCharacters(type):

    registered_characters = []

    def __new__(cls, clsname, bases, attrs):
        newclass = super().__new__(cls, clsname, bases, attrs)
        cls.register_new_class(newclass)

        return newclass

    @classmethod
    def register_new_class(cls, newcharacter):
        characters_infos = (newcharacter.slug, newcharacter.name, newcharacter)
        if not all(characters_infos):
            return
        cls.registered_characters.append(characters_infos)


class Character(object, metaclass=RegisteredCharacters):
    name = None
    slug = None
    start_permissions = []


class EmptyCharacter(Character):

    class Meta:
        proxy = True


class Unknown(EmptyCharacter):
    name = 'Undefined'
    slug = 'NONE'
    start_permissions = []


class Villager(EmptyCharacter):
    name = 'Human'
    slug = 'HUMA'
    start_permissions = [
        "Game.can_elect",
        "Game.can_vote",
    ]


class Werewolf(EmptyCharacter):
    name = 'Werewolf'
    slug = 'WOLF'
    start_permissions = [
        "Game.can_elect",
        "Game.can_vote",
        "Game.can_murder",
    ]


class Seer(EmptyCharacter):
    name = 'Seer'
    slug = 'SEER'
    start_permissions = [
        "Game.can_elect",
        "Game.can_vote",
        "Game.can_predict",
    ]


class Cupidon(EmptyCharacter):
    name = 'Cupidon'
    slug = 'CUPD'
    start_permissions = [
        "Game.can_elect",
        "Game.can_vote",
        "Game.can_link",
    ]


class Witch(EmptyCharacter):
    name = 'Witch'
    slug = 'WTCH'
    start_permissions = [
        "Game.can_elect",
        "Game.can_vote",
        "Game.can_save",
        "Game.can_poison",
    ]
