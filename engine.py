import pygame
from enum import Enum, auto
import data
import loading
import math_operations


_all_sprites = pygame.sprite.Group()
_tile_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()

_character_sprites = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_enemy_sprites = pygame.sprite.Group()

_bullet_sprites = pygame.sprite.Group()
_melee_hit = pygame.sprite.Group()

_item_sprites = pygame.sprite.Group()
_equipped_item_sprites = pygame.sprite.Group()

_pause_sprites = pygame.sprite.Group()
_menu_sprites = pygame.sprite.Group()

_map_items_sprites = pygame.sprite.Group()
_open_door_sprites = pygame.sprite.Group()
_close_door_sprites = pygame.sprite.Group()

PLAYER_POS = 0, 0


class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    WIN = auto()
    LOSE = auto()


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.x1, self.x2, self.y1, self.y2 = pos[0], pos[0] + 2, pos[1], pos[1] + 1
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.tile_width * self.x1, data.tile_height * self.y1)

    def is_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0] / data.tile_width
        mouse_y = pygame.mouse.get_pos()[1] / data.tile_height
        if self.x1 <= mouse_x <= self.x2 and self.y1 <= mouse_y <= self.y2:
            return True
        return False


class Creature(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self.weapon_inventory, self.equipped = [''], ''
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.tile_width * self.x, data.tile_height * self.y)
        self.vx, self.vy = 0, 0
        self.durability = data.hp

    def update(self, *events, kill=False):
        if kill:
            self.kill()

    def update_image(self, direction_changed):
        self.image = pygame.transform.flip(self.orig_image, True, False) if direction_changed \
            else self.orig_image

    def update_pos(self):
        self.pos = self.x, self.y = self.rect.x / data.tile_width, self.rect.y / data.tile_height

    def change_equipped_item(self, event):
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.remove(self.equipped)
        self.equipped = self.weapon_inventory[
            (self.weapon_inventory.index(self.equipped) +
             (1 if event.button == pygame.BUTTON_WHEELUP else -1)) % len(self.weapon_inventory)]
        if isinstance(self.equipped, Item):
            _equipped_item_sprites.add(self.equipped)


class Player(Creature):
    def __init__(self, pos, *groups):
        super().__init__('player', pos, *groups)
        self.weapon_inventory = ['', RangeWeapon('bow', self.pos, _item_sprites),
                                 MeleeWeapon('sword', self.pos, _item_sprites)]
        self.keys_inventory = 0

    def update(self, *events, kill=False):
        if kill:
            self.kill()
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
        if pygame.sprite.spritecollideany(self, _map_items_sprites) and _map_items_sprites.has(self):
            pygame.sprite.spritecollideany(self, _map_items_sprites).kill()
            self.keys_inventory += 1
        if pygame.sprite.spritecollideany(self, _close_door_sprites) and _close_door_sprites.has(self) and self.keys_inventory:
            pass

    def attack(self):
        if self.equipped and isinstance(self.equipped, Weapon):
            if isinstance(self.equipped, RangeWeapon):
                self.equipped.shoot(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                                    / 50, pygame.mouse.get_pos()[1] / 50))
            elif isinstance(self.equipped, MeleeWeapon):
                self.equipped.hit(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                                    / 50, pygame.mouse.get_pos()[1] / 50))

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
        global PLAYER_POS
        self.pos = self.x, self.y = self.rect.x / data.tile_width,\
                                    self.rect.y / data.tile_height
        PLAYER_POS = self.pos[:]
        for item in self.weapon_inventory:
            if isinstance(item, Item):
                item.update_pos(self.x + (self.rect.width - item.rect.width) // 2 /
                                data.tile_width, self.y + 5 / data.tile_height)


class Enemy(Creature):
    def __init__(self, pos, *groups):
        super().__init__('enemy', pos, *groups)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -3 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -3 if self.vy else 0)
        if pygame.sprite.spritecollideany(self, _bullet_sprites) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _bullet_sprites).kill()
            self.durability -= 7
        if pygame.sprite.spritecollideany(self, _melee_hit) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _melee_hit).kill()
            self.durability -= 17
        if self.durability <= 0:
            self.kill()

    def move(self):
        if self.x < PLAYER_POS[0]:
            self.vx = data.NPC_SPEED
        if self.x > PLAYER_POS[0]:
            self.vx = -data.NPC_SPEED
        if self.y < PLAYER_POS[1]:
            self.vy = data.NPC_SPEED
        if self.y > PLAYER_POS[1]:
            self.vy = -data.NPC_SPEED

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

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, -angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

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
        Bullet('arrow', (self.x + 15 / data.tile_width, self.y + 11 / data.tile_height), angle, _bullet_sprites)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        angle = math_operations.calculate_angle(self.x * data.tile_width, self.y * data.tile_height, *pygame.mouse.get_pos())
        self.image, self.rect = self.rotate(self.orig_image, self.rect, angle)


class MeleeWeapon(Weapon):
    def hit(self, look_target):
        Bullet('arrow', (self.x + 15 / data.tile_width, self.y + 11 / data.tile_height),
               look_target, _melee_hit, not_bullet=True)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.update_image(0 if self.pos[0] <= pygame.mouse.get_pos()[0] / 50 else 1)

    def update_image(self, direction):
        if direction == 1:
            self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, angle, *groups, not_bullet=False):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.is_not_bullet = not_bullet
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
        self.durability = 3

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        if self.is_not_bullet:
            self.durability -= 1
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable) or self.durability <= 0:
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

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)

    def _init_sprite(self,sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.tile_size[0] * self.x,
                                               data.tile_size[1] * self.y)


class Door(Tile):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(sprite_type, pos, *groups)


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
