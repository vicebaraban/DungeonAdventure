import pygame
from enum import Enum, auto
import math_operations
import data


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_bullet_sprites = pygame.sprite.Group()
_item_sprites = pygame.sprite.Group()


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_size[0] * pos[0],
                                               data.tile_size[1] * pos[1])
        self.vx, self.vy = 0, 0

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -2 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -2 if self.vy else 0)


class Character:
    def __init__(self, sprite_type, pos, *groups):
        self._sprite = Sprite(sprite_type, pos, groups)
        self.position = self.x, self.y = pos
        self.angle = 0
        self.inventory = ['']
        self.equipped = ''

    def look(self, target_pos):
        self.angle = math_operations.calculate_angle(*self.position, *target_pos)

    def get_pos(self):
        return self.position

    def get_angle(self):
        return self.angle

    def change_equipped_item(self):
        self.equipped = self.inventory[(self.inventory.index(self.equipped) + 1) %
                                       len(self.inventory)]

    def attack(self, target):
        if self.equipped and isinstance(self.equipped, Weapon):
            if isinstance(self.equipped, RangeWeapon):
                self.equipped.shoot(...)
            elif isinstance(self.equipped, MeleeWeapon):
                self.equipped.hit(...)

    def move(self, direction: MoveDirection):
        pass


class Player(Character):
    def __init__(self, pos):
        super().__init__('player', pos, _player_sprites)

    def pick(self):
        pass

    def select(self):
        pass

    def drop(self):
        pass

    def use(self):
        pass

    def reload(self):
        pass


class NPC(Character):
    pass


class Item:
    def __init__(self, sprite_type, pos):
        self._sprite = Sprite(sprite_type, pos, _item_sprites)
        self.position = self.x, self.y = pos

    def use(self):
        pass

    def drop(self):
        pass

    def select(self):
        pass


class Weapon(Item):
    def attack(self):
        pass


class RangeWeapon(Weapon):
    def shoot(self):
        pass

    def reload(self):
        pass


class MeleeWeapon(Weapon):
    def hit(self):
        pass


class Bullet:
    def __init__(self, sprite_type, pos):
        self._sprite = Sprite(sprite_type, pos, _bullet_sprites)
        self.position = self.x, self.y = pos
        self.angle = 0


class Menu:
    pass


class MainMenu(Menu):
    pass


class PauseMenu(Menu):
    pass


class Map:
    pass
