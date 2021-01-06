import pygame
from enum import Enum, auto
import math_operations
import data
import loading


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()


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

    def look_away(self, additional_coords):
        angle = math_operations.calculate_angle(*self.position, *additional_coords)
        return angle


class Player(Character):
    def __init__(self, pos):
        super().__init__('player', pos, _player_sprites)

    # def draw(self, surface: pygame.Surface):
    #     print(self.look_away(pygame.mouse.get_pos()))
    #     # self.image = pygame.transform.rotate(self.image,
    #     #                                      self.look_away(pygame.mouse.get_pos()))
    #     self._sprite.draw(surface)

    def move(self, direction: MoveDirection):
        if direction == MoveDirection.UP:
            self.position = math_operations.change_position(
                self.position, angle, data.MAIN_CHAR_SPEED, 1)
        elif direction == MoveDirection.DOWN:
            self.position = math_operations.change_position(
                self.position, angle, data.MAIN_CHAR_SPEED, 2)
        elif direction == MoveDirection.LEFT:
            self.position = math_operations.change_position(
                self.position, angle, data.MAIN_CHAR_SPEED, 3)
        else:
            self.position = math_operations.change_position(
                self.position, angle, data.MAIN_CHAR_SPEED, 4)


class NPC(Character):
    pass


class Item:
    pass


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
