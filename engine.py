import pygame
from enum import Enum, auto
import math_operations
import data


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_equipped_item_sprites = pygame.sprite.Group()
_bullet_sprites = pygame.sprite.Group()
_item_sprites = pygame.sprite.Group()
_character_sprites = pygame.sprite.Group()


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
        self._sprite = Sprite(sprite_type, pos, _character_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self.inventory = ['']
        self.equipped = ''

    def look(self, target_pos):
        self.angle = math_operations.calculate_angle(*self.pos, *target_pos)

    def get_pos(self):
        return self.pos

    def get_angle(self):
        return self.angle

    def change_equipped_item(self, event):
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.remove(self.equipped._sprite)
        self.equipped = self.inventory[(self.inventory.index(self.equipped) +
                                        (1 if event.button == pygame.BUTTON_WHEELUP else -1)) %
                                       len(self.inventory)]
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.add(self.equipped._sprite)

    def attack(self, target):
        if self.equipped and isinstance(self.equipped, Weapon):
            if isinstance(self.equipped, RangeWeapon):
                self.equipped.shoot(...)
            elif isinstance(self.equipped, MeleeWeapon):
                self.equipped.hit(...)

    def move(self, direction: MoveDirection):
        pass

    def update_pos(self):
        self.pos = self._sprite.rect.x / data.tile_width, self._sprite.rect.y / data.tile_height


class Player(Character):
    def __init__(self, pos):
        super().__init__('player', pos, _player_sprites)
        self.inventory = ['', RangeWeapon('bow', self.pos), MeleeWeapon('sword', self.pos)]

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

    def move(self, event):
        if event.key == pygame.K_w:
            self._sprite.vy -= data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_a:
            self._sprite.vx -= data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_s:
            self._sprite.vy += data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_d:
            self._sprite.vx += data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)

    def update_pos(self):
        self.pos = self.x, self.y = self._sprite.rect.x / data.tile_width,\
                                    self._sprite.rect.y / data.tile_height
        for item in self.inventory:
            if isinstance(item, Item):
                item.update_pos(self.x, self.y)


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

    def update_pos(self, x, y):
        print(x, y)
        self._sprite.rect = self._sprite.image.get_rect().move(x * data.tile_width, y * data.tile_height)


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
