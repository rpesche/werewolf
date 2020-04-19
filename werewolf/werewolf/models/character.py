
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
        "Game.can_vote_mayor",
        "Game.can_vote_hanged",
    ]


class Werewolf(EmptyCharacter):
    name = 'Werewolf'
    slug = 'WOLF'
    start_permissions = [
        "Game.can_vote_mayor",
        "Game.can_vote_hanged",
        "Game.can_vote_murdered",
    ]
