import pygame
from enum import Enum, auto
import math_operations
import constants


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Character:
    def __init__(self, position):
        self.position = position

    def look_away(self, additional_coords):
        angle = math_operations.calculate_angle(*self.position, *additional_coords)
        return angle


class CharacterSprite(pygame.sprite.GroupSingle):
    def __init__(self, image_name):
        super().__init__()
        char_sprite = pygame.sprite.Sprite()
        char_sprite.rect = pygame.Rect(0, 0, 80, 80)
        char_sprite.image = pygame.transform.scale(
            pygame.image.load(image_name),
            char_sprite.rect.size)
        self.add(char_sprite)


class PlayerCharacter(Character):
    def __init__(self, position):
        super().__init__(position)
        self._sprite = CharacterSprite('character.png')

    def draw(self, surface: pygame.Surface):
        self._sprite = pygame.transform.rotate(self._sprite,
                                               self.look_away(pygame.mouse.get_pos()))
        self._sprite.draw(surface.subsurface(0, 0, 80, 80))

    def move(self, direction: MoveDirection):
        angle = self.look_away(pygame.mouse.get_pos())
        if direction == MoveDirection.UP:
            self.position = math_operations.change_position(
                self.position, angle, constants.MAIN_CHAR_SPEED, 1)
        elif direction == MoveDirection.DOWN:
            self.position = math_operations.change_position(
                self.position, angle, constants.MAIN_CHAR_SPEED, 2)
        elif direction == MoveDirection.LEFT:
            self.position = math_operations.change_position(
                self.position, angle, constants.MAIN_CHAR_SPEED, 3)
        else:
            self.position = math_operations.change_position(
                self.position, angle, constants.MAIN_CHAR_SPEED, 4)


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
