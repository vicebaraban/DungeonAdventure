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
_non_attack_bullet_sprites = pygame.sprite.Group()
_melee_hit = pygame.sprite.Group()
_item_sprites = pygame.sprite.Group()
_character_sprites = pygame.sprite.Group()
_enemy_sprites = pygame.sprite.Group()
_pause_sprites = pygame.sprite.Group()
_menu_sprites = pygame.sprite.Group()
_map_items_sprites = pygame.sprite.Group()
_door_sprites = pygame.sprite.Group()
_open_door_sprites = pygame.sprite.Group()
_close_door_sprites = pygame.sprite.Group()
_bar_sprites = pygame.sprite.Group()
_interface_sprites = pygame.sprite.Group()


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
        self.rect = self.image.get_rect().move(data.TITLE_WIDTH * self.x1, data.TITLE_HEIGHT * self.y1)

    def is_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0] / data.TITLE_HEIGHT
        mouse_y = pygame.mouse.get_pos()[1] / data.TITLE_WIDTH
        if self.x1 <= mouse_x <= self.x2 and self.y1 <= mouse_y <= self.y2:
            return True
        return False


class Creature(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)
        self.vx, self.vy = 0, 0
        self.durability = data.HP

    def get_state(self):
        return

    def update(self, *events, kill=False):
        if kill:
            self.kill()

    def update_image(self, direction):
        if direction == 1:
            self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image

    def update_pos(self):
        self.pos = self.x, self.y = self.rect.x / data.TITLE_WIDTH, self.rect.y / data.TITLE_HEIGHT


class Player(Creature):
    def __init__(self, pos, *groups):
        super().__init__('player', pos, *groups)
        self.inventory = Inventory(['hand', RangeWeapon('bow', self.pos, _item_sprites),
                                    MeleeWeapon('sword', self.pos, _item_sprites)])
        self.keys_inventory = 0
        self.char_state = GameState.PLAYING
        self.sword_cooldown = data.SWORD_COOLDOWN
        self.bow_cooldown = data.BOW_COOLDOWN
        self.close_hit_cooldown = data.CLOSE_HIT_COOLDOWN
        self.player_health_bar = HeathBar((0.5, 0.5), 'health_bar', self.durability)

    def update_cooldowns(self):
        if self.sword_cooldown >= data.SWORD_COOLDOWN:
            self.sword_cooldown = 0
        elif self.sword_cooldown != 0:
            self.sword_cooldown += 1
        if self.bow_cooldown >= data.BOW_COOLDOWN:
            self.bow_cooldown = 0
        elif self.bow_cooldown != 0:
            self.bow_cooldown += 1
        if self.close_hit_cooldown >= data.CLOSE_HIT_COOLDOWN:
            self.close_hit_cooldown = 0
        else:
            self.close_hit_cooldown += 1

    def update(self, *events, kill=False):
        #print(self.inventory.equipped())
        if kill:
            self.kill()
        self.player_health_bar.take_current_health(self.durability)
        self.update_cooldowns()
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
        if pygame.sprite.spritecollideany(self, _enemy_sprites) and self.close_hit_cooldown == 0:
            self.durability -= 3
            data.char_hit_sound.play()
            print(self.durability)
        if self.durability <= 0:
            self.durability = 0
            self.char_state = GameState.LOSE
            data.playing_music.stop()
            pygame.mixer.Channel(0).play(data.lose_music)

    def init_health_bar(self):
        pass

    def get_state(self):
        return self.char_state

    def attack(self):
        print(self.inventory.storage)
        equipped = self.inventory.equipped()
        if equipped and isinstance(equipped, Tool):
            if isinstance(equipped, RangeWeapon) and self.bow_cooldown == 0:
                equipped.shoot(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                                    / 50, pygame.mouse.get_pos()[1] / 50))
                self.bow_cooldown += 1
                data.bow_shoot_sound.play()
            elif isinstance(equipped, MeleeWeapon) and self.sword_cooldown == 0:
                equipped.hit(math_operations.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                                    / 50, pygame.mouse.get_pos()[1] / 50))
                self.sword_cooldown += 1
                data.sword_hit_sound.play()
        elif equipped == 'hand':
            if pygame.sprite.spritecollideany(self, _map_items_sprites):
                pygame.sprite.spritecollideany(self, _map_items_sprites).kill()
                self.inventory.add_item('key')
                data.take_item_sound.play()
                print(self.keys_inventory)
        elif pygame.sprite.spritecollideany(self, _close_door_sprites) and equipped == 'key':
            _close_door_sprites.update(activate=True)
            del self.inventory.storage[self.inventory.get_index()]
            print(1)

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
        self.pos = self.x, self.y = self.rect.x / data.TITLE_WIDTH, self.rect.y / data.TITLE_HEIGHT
        PLAYER_POS = self.pos[:]
        self.inventory.update_tools_pos(self.x, self.y, self.rect)

    def change_equipped_item(self, event):
        if event.key == pygame.K_1:
            position = 0
        elif event.key == pygame.K_2:
            position = 1
        elif event.key == pygame.K_3:
            position = 2
        elif event.key == pygame.K_4:
            position = 3
        elif event.key == pygame.K_5:
            position = 4
        elif event.key == pygame.K_6:
            position = 5
        elif event.key == pygame.K_7:
            position = 6
        elif event.key == pygame.K_8:
            position = 7
        elif event.key == pygame.K_9:
            position = 8
        else:
            position = 9
        self.inventory.take_active_tool(position)
        # self.equipped = self.inventory[(self.inventory.index(self.equipped) +
        #                                 (1 if event.button == pygame.BUTTON_WHEELUP else -1)) %
        #                                len(self.inventory)]


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
            data.enemy_hit_sound.play()
            self.kill()

    def move(self):
        if self.target_distance(PLAYER_POS) <= 3:
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


class Inventory:
    def __init__(self, items):
        self.storage = [*items]
        print(self.storage)
        self.active_position = 0

    def update(self):
        pass

    def take_active_tool(self, position):
        if isinstance(self.storage[self.active_position], Item):
            _equipped_item_sprites.remove(self.storage[self.active_position])
        self.active_position = position if position + 1 <= len(self.storage) else 0
        if isinstance(self.storage[self.active_position], Item):
            _equipped_item_sprites.add(self.storage[self.active_position])

    def add_item(self, item):
        self.storage.append(item)

    def get_index(self):
        return self.active_position

    def equipped(self):
        return self.storage[self.active_position] if self.storage else None

    def update_tools_pos(self, x, y, rect):
        for tool in self.storage:
            if isinstance(tool, Item):
                tool.update_pos(x + (rect.width - tool.rect.width) // 2 /
                                data.TITLE_WIDTH, y + 5 / data.TITLE_HEIGHT)


class Interface(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(_all_sprites, _interface_sprites, *groups)
        self.pos = self.x, self.y = pos

    def update(self, *events, kill=False):
        if kill:
            self.kill()


class HeathBar(Interface):
    def __init__(self, pos, sprite_type, health):
        super().__init__(pos, _bar_sprites)
        self.max_health = self.health = health
        self.image = data.images[sprite_type]
        self.image = pygame.transform.scale(self.image, (160, 30))
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.image = pygame.transform.scale(self.image, (160 * self.health // self.max_health, 30))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)

    def take_current_health(self, health):
        self.health = health if health > 0 else 0


class SkillBar(Interface):
    pass


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(_all_sprites, _item_sprites, *groups)
        self.pos = self.x, self.y = pos
        self._init_sprite(sprite_type)

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)
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

    def use(self):
        pass

    def drop(self):
        pass

    def select(self):
        pass

    def update_pos(self, x, y):
        self.rect = self.image.get_rect().move(x * data.TITLE_WIDTH, y * data.TITLE_HEIGHT)
        self.pos = self.x, self.y = self.rect.x / data.TITLE_WIDTH, self.rect.y / data.TITLE_HEIGHT


class Key(Item):
    def __init__(self, pos, *groups):
        super().__init__('key', pos, *groups)
        self.pos = self.x, self.y = pos


class Tool(Item):
    pass


class RangeWeapon(Tool):
    def shoot(self, angle):
        Bullet('arrow', (self.x + 15 / data.TITLE_WIDTH, self.y + 11 / data.TITLE_HEIGHT), angle, _bullet_sprites)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        angle = math_operations.calculate_angle(self.x * data.TITLE_WIDTH,
                                                self.y * data.TITLE_HEIGHT, *pygame.mouse.get_pos())
        self.image, self.rect = self.rotate(self.orig_image, self.rect, angle)


class MeleeWeapon(Tool):
    def hit(self, look_target):
        Bullet('arrow', (self.x + 15 / data.TITLE_WIDTH, self.y + 11 / data.TITLE_HEIGHT),
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


# class Hand:
#     def __init__(self, pos):
#         self.pos = self.x, self.y = pos
#
#     def interaction(self, look_target):
#         Bullet('arrow', (self.x + 15 / data.TITLE_WIDTH, self.y + 11 / data.TITLE_HEIGHT),
#                look_target, _non_attack_bullet_sprites, not_bullet=True)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos, angle, *groups, not_bullet=False):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.is_not_bullet = not_bullet
        self.vx, self.vy = math_operations.change_position(math_operations.calculate_angle(pos[0] * data.TITLE_WIDTH,
                                                                                           pos[1] * data.TITLE_HEIGHT,
                                                                                           *pygame.mouse.get_pos()),
                                                           data.BULLET_SPEED, 1)
        self.angle = angle
        if _melee_hit in groups:
            self.durability = 3
        elif _non_attack_bullet_sprites in groups:
            self.durability = 2
        else:
            self.durability = 10
        self._init_sprite(sprite_type)
        print(self.durability)

    def _init_sprite(self, sprite_type):
        self.image = data.images[sprite_type]
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)
        self.image, self.rect = self.rotate(self.image, self.rect, self.angle)

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
            x * data.TITLE_WIDTH, y * data.TITLE_HEIGHT)
        self.pos = self.x, self.y = self.rect.x / data.TITLE_WIDTH, self.rect.y / data.TITLE_HEIGHT


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

    def _init_sprite(self, sprite_type):
        self.orig_image = data.images[sprite_type]
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(data.TITLE_SIZE[0] * self.x,
                                               data.TITLE_SIZE[1] * self.y)


class Door(Tile):
    def __init__(self, sprite_type, pos, *groups):
        super().__init__(sprite_type, pos, *groups)
        self.durability = 2

    def update(self, *events, kill=False, activate=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / data.FPS, self.vy / data.FPS)
        if activate:
            self.durability -= 1
        if self.durability == 0:
            self.kill()


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
        if obj not in _interface_sprites:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - data.WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - data.HEIGHT // 2)
