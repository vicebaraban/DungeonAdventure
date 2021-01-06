import pygame
from enum import Enum, auto
import math_operations
import data
import loading


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_bullets = pygame.sprite.Group()


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, groups):
        super().__init__(_all_sprites, *groups)
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_size[0] * pos[0],
                                               data.tile_size[1] * pos[1])
        self.vx, self.vy = 0, 0

    def update(self, *args):
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
        self.inventory = {'first_weapon': 'pistol', 'second_gun': 'rifle'}

    def look_away(self, additional_coords):
        angle = math_operations.calculate_angle(*self.position, *additional_coords)
        return angle

    def get_pos(self):
        return self.position

    def get_angle(self):
        return self.angle

    def _select_weapon(self, mode):
        if mode == 1:
            weapon = self.inventory['first_weapon']
        elif mode == 2:
            weapon = self.inventory['second_weapon']
        # ...
        else:
            weapon = None
        return weapon

    def attack(self, mode):
        weapon = self._select_weapon(mode)
        if weapon is not None:
            if weapon == 'pistol':
                bullet = Bullet(*self.position, ...)
                _all_sprites.add(bullet)
                _bullets.add(bullet)


class Player(Character):
    def __init__(self, pos):
        super().__init__('player', pos, _player_sprites)

    # def draw(self, surface: pygame.Surface):
    #     print(self.look_away(pygame.mouse.get_pos()))
    #     self.image = pygame.transform.rotate(self.image,
    #                                            self.look_away(pygame.mouse.get_pos()))
    #     self._sprite.draw(surface)
    #     self._sprite.draw(surface.subsurface(0, 0, 80, 80))

    def update(self): # будет вызываться в render_screen
        self.angle = self.look_away(pygame.mouse.get_pos())
        # self.draw()
        # ...

    def move(self, direction: MoveDirection): # возможно стоит перенести в Character
        pass # из main перенести операции сюда


class NPC(Character):
    pass


class Item:
    pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_type, pos, groups):
        pygame.sprite.Sprite.__init__(self)
        self._sprite = Sprite(sprite_type, pos, groups)
        self._start_position = x, y
        self._time = data.BULLET_TIME
        self._speed = data.BULLET_SPEED

    def draw(self):
        # self._sprite.move(...) используя данные f change_position(.., direction=1)
        pass

    def update(self): # аналогично с Character
        self.draw()


class Weapon(Item):
    pass


class Menu:
    pass


class MainMenu(Menu):
    pass


class PauseMenu(Menu):
    pass


class Map:
    pass
