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
_npc_sprites = pygame.sprite.Group()
_button_sprites = pygame.sprite.Group()


class MoveDirection(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSE = auto()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, angle, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_size[0] * pos[0],
                                               data.tile_size[1] * pos[1])
        self.image, self.rect = self.rotate(self.image, self.rect, -angle)
        self.vx, self.vy = 0, 0

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -2 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -2 if self.vy else 0)

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect


class BulletSprite(Sprite):
    def __init__(self, angle, v, sprite_type, pos, *groups):
        super().__init__(angle, sprite_type, pos, *groups)
        self.vx, self.vy = v

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)


class Button:
    def __init__(self, sprite_type, pos, *groups):
        self._sprite = Sprite(0, sprite_type, pos, _button_sprites, *groups)
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = pos[0] + 30
        self.y2 = pos[1] + 30

    def is_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0] - 250
        mouse_y = pygame.mouse.get_pos()[1] - 250
        if self.x1 <= mouse_x <= self.x2 and self.y1 <= mouse_y <= self.y2:
            return True
        return False


class Character:
    def __init__(self, sprite_type, pos, *groups):
        self._sprite = Sprite(0, sprite_type, pos, _character_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self.inventory = ['']
        self.equipped = ''

    def get_pos(self):
        return self.pos

    def look(self, target_pos):
        self.angle = math_operations.calculate_angle(*self.pos, *target_pos)

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

    def move(self, direction: MoveDirection):
        pass

    def update_pos(self):
        self.pos = self._sprite.rect.x / data.tile_width, self._sprite.rect.y / data.tile_height


class Player(Character):
    def __init__(self, pos):
        super().__init__('player', pos, _player_sprites)
        self.inventory = ['', RangeWeapon('bow', self.pos),
                          MeleeWeapon('sword', self.pos)]

    def attack(self):
        if self.equipped and isinstance(self.equipped, Weapon):
            if isinstance(self.equipped, RangeWeapon):
                print(self.pos, pygame.mouse.get_pos())
                self.equipped.shoot(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0] - 250, pygame.mouse.get_pos()[1] - 250))
            elif isinstance(self.equipped, MeleeWeapon):
                pass
                # self.equipped.hit(...)

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
                item.update_pos(self.x + 35 / data.tile_width, self.y + 5 / data.tile_height)


class Enemy(Character):
    def __init__(self, pos):
        super().__init__('enemy', pos, _npc_sprites)
        self.position = pos

    def target_distance(self, pos):
        return math_operations.hypotenuse(*self.position, *pos)


class Item:
    def __init__(self, sprite_type, pos):
        self._sprite = Sprite(0, sprite_type, pos, _item_sprites)
        self.pos = self.x, self.y = pos

    def use(self):
        pass

    def drop(self):
        pass

    def select(self):
        pass

    def update_pos(self, x, y):
        self._sprite.rect = self._sprite.image.get_rect().move(x * data.tile_width, y * data.tile_height)
        self.pos = self.x, self.y = self._sprite.rect.x / data.tile_width, self._sprite.rect.y / data.tile_height


class Weapon(Item):
    def attack(self):
        pass


class RangeWeapon(Weapon):
    def shoot(self, angle):
        Bullet('arrow', (self.x - 3 / data.tile_width, self.y + 11 / data.tile_height), angle)

    def reload(self):
        pass


class MeleeWeapon(Weapon):
    def hit(self):
        pass


class Bullet:
    def __init__(self, sprite_type, pos, angle):
        self._sprite = BulletSprite(angle, math_operations.change_position(
            math_operations.calculate_angle(pos[0] * data.tile_width, pos[1] * data.tile_height, *pygame.mouse.get_pos()),
            data.BULLET_SPEED, 1), sprite_type, pos, _bullet_sprites)
        self.pos = self.x, self.y = pos

    def update_pos(self, x, y):
        self._sprite.rect = self._sprite.image.get_rect().move(
            x * data.tile_width, y * data.tile_height)
        self.pos = self.x, self.y = self._sprite.rect.x / data.tile_width, self._sprite.rect.y / data.tile_height


class Map:
    pass
