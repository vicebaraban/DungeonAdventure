import pygame
from enum import Enum, auto
import data
import loading
import math_operations


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_equipped_item_sprites = pygame.sprite.Group()
_bullet_sprites = pygame.sprite.Group()
_item_sprites = pygame.sprite.Group()
_character_sprites = pygame.sprite.Group()
_enemy_sprites = pygame.sprite.Group()
_pause_button_sprites = pygame.sprite.Group()
_menu_button_sprites = pygame.sprite.Group()
_button_sprites = pygame.sprite.Group()
_map_items_sprites = pygame.sprite.Group()
_door_sprites = pygame.sprite.Group()


class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSE = auto()


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.x1 = pos[0]
        self.y1 = pos[1]
        self.x2 = pos[0] + 2
        self.y2 = pos[1] + 1
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x1,
                                               data.tile_size[1] * self.y1)

    def is_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0] / 50
        mouse_y = pygame.mouse.get_pos()[1] / 50
        if self.x1 <= mouse_x <= self.x2 and self.y1 <= mouse_y <= self.y2:
            return True
        return False


class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self.inventory = ['']
        self.equipped = ''
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x,
                                               data.tile_size[1] * self.y)
        self.vx, self.vy = 0, 0
        self.durability = 20

    def update(self, *events):
        pass

    def update_image(self, direction):
        if direction == 1:
            self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image

    def update_pos(self):
        self.pos = self.rect.x / data.tile_width, self.rect.y / data.tile_height

    def look(self, target_pos):
        self.angle = math_operations.calculate_angle(*self.pos, *target_pos)

    def change_equipped_item(self, event):
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.remove(self.equipped)
        self.equipped = self.inventory[(self.inventory.index(self.equipped) +
                                        (1 if event.button == pygame.BUTTON_WHEELUP else -1)) %
                                       len(self.inventory)]
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.add(self.equipped)


class Player(Character):
    def __init__(self, pos, *groups):
        super().__init__('player', pos, *groups)
        self.inventory = ['', RangeWeapon('bow', self.pos, _item_sprites),
                          MeleeWeapon('sword', self.pos, _item_sprites)]

    def update(self, *events):
        self.update_image(0 if self.pos[0] <= pygame.mouse.get_pos()[0] / 50 else 1)
        self.rect = self.rect.move(self.vx / data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -3 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -3 if self.vy else 0)
        if pygame.sprite.spritecollideany(self, _bullet_sprites) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _bullet_sprites).kill()
            self.durability -= 7
            if self.durability <= 0:
                self.kill()

    def attack(self):
        if self.equipped and isinstance(self.equipped, Weapon):
            if isinstance(self.equipped, RangeWeapon):
                self.equipped.shoot(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                                    / 50, pygame.mouse.get_pos()[1] / 50))
            elif isinstance(self.equipped, MeleeWeapon):
                pass
                # self.equipped.hit(...)

    def move(self, event):
        if event.key == pygame.K_w:
            self.vy -= data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_a:
            self.vx -= data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_s:
            self.vy += data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_d:
            self.vx += data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)

    def update_pos(self):
        self.pos = self.x, self.y = self.rect.x / data.tile_width,\
                                    self.rect.y / data.tile_height
        for item in self.inventory:
            if isinstance(item, Item):
                item.update_pos(self.x + 35 / data.tile_width, self.y + 5 / data.tile_height)


class Enemy(Character):
    def __init__(self, pos, *groups):
        super().__init__('enemy', pos, *groups)

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -3 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -3 if self.vy else 0)
        if pygame.sprite.spritecollideany(self, _bullet_sprites) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _bullet_sprites).kill()
            self.durability -= 7
            if self.durability <= 0:
                self.kill()

    def target_distance(self, pos):
        return math_operations.hypotenuse(*self.pos, *pos)


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, _item_sprites, *groups)
        self.pos = self.x, self.y = pos
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x,
                                               data.tile_size[1] * self.y)
        self.vx, self.vy = 0, 0
        self.durability = 20

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, -angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def use(self):
        pass

    def drop(self):
        pass

    def select(self):
        pass

    def update_pos(self, x, y):
        self.rect = self.image.get_rect().move(x * data.tile_width, y * data.tile_height)
        self.pos = self.x, self.y = self.rect.x / data.tile_width, self.rect.y / data.tile_height


class Key(Item):
    def __init__(self, pos, *groups):
        super().__init__('key', pos, *groups)
        self.pos = self.x, self.y = pos


class Weapon(Item):
    pass


class RangeWeapon(Weapon):
    def shoot(self, angle):
        Bullet('arrow', (self.x - 3 / data.tile_width, self.y + 11 / data.tile_height), angle, _bullet_sprites)

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        angle = math_operations.calculate_angle(self.x * data.tile_width, self.y * data.tile_height, *pygame.mouse.get_pos())
        self.image, self.rect = self.rotate(self.orig_image, self.rect, angle)


class MeleeWeapon(Weapon):
    def hit(self):
        pass

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        angle = math_operations.calculate_angle(self.x * data.tile_width, self.y * data.tile_height,
                                                *pygame.mouse.get_pos())
        self.image, self.rect = self.rotate(self.orig_image, self.rect, angle)
        self.vx, self.vy = math_operations.change_position(angle, 20, 1)
        self.update_image(0 if self.pos[0] <= pygame.mouse.get_pos()[0] / 50 else 1)

    def update_image(self, direction):
        if direction == 1:
            self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, angle, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.vx, self.vy = math_operations.change_position(math_operations.calculate_angle(pos[0] * data.tile_width,
                                                                                           pos[1] * data.tile_height,
                                                                                           *pygame.mouse.get_pos()),
                                                           data.BULLET_SPEED, 1)
        self.angle = angle
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x,
                                               data.tile_size[1] * self.y)
        self.image, self.rect = self.rotate(self.image, self.rect, self.angle)
        self.durability = 20

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.kill()

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, -angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def update_pos(self, x, y):
        self.rect = self.image.get_rect().move(
            x * data.tile_width, y * data.tile_height)
        self.pos = self.x, self.y = self.rect.x / data.tile_width, self.rect.y / data.tile_height


class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self._init_sprite(sprite_type)
        self.vx, self.vy = 0, 0

    def update(self, *events):
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)

    def _init_sprite(self,sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x,
                                               data.tile_size[1] * self.y)


class Door(Tile):
    def __init__(self, is_open, pos, *groups):
        super().__init__('door_opened' if is_open else 'door_closed', pos, *groups)


class GameMap:
    def __init__(self, level):
        self._map = loading.load_level(level)
        self.start_pos = loading.generate_level(self._map)

    def draw(self, screen):
        _tile_sprites.draw(screen)
        _map_items_sprites.draw(screen)
        _character_sprites.draw(screen)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - data.WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - data.HEIGHT // 2)
