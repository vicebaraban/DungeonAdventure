class Character:
    def __init__(self, pos):
        self.pos = self.x, self.y = pos


class Player(Character):
    pass


class NPC(Character):
    pass


class Item:
    def __init__(self, pos):
        self.pos = self.x, self.y = pos


class Weapon(Item):
    pass


class Menu:
    def __init__(self):
        pass


class MainMenu(Menu):
    pass


class PauseMenu(Menu):
    pass


class Map:
    def __init__(self):
        pass
