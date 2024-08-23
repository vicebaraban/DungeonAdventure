import pygame
from enum import Enum, auto
import engine_main, engine_math, engine_loading
import game_data


PLAYER_POS = 0, 0

_tile_sprites = pygame.sprite.Group()
_player_sprites = pygame.sprite.Group()
_equipped_item_sprites = pygame.sprite.Group()
_bullet_sprites = pygame.sprite.Group()
_character_sprites = pygame.sprite.Group()
_enemy_sprites = pygame.sprite.Group()
_pause_sprites = pygame.sprite.Group()
_menu_sprites = pygame.sprite.Group()
_level_sprites = pygame.sprite.Group()
_map_items_sprites = pygame.sprite.Group()
_door_sprites = pygame.sprite.Group()
_open_door_sprites = pygame.sprite.Group()
_close_door_sprites = pygame.sprite.Group()
_bar_sprites = pygame.sprite.Group()
_icon_tool_interface_sprites = pygame.sprite.Group()
_impenetrable = pygame.sprite.Group()
_non_attack_bullet_sprites = pygame.sprite.Group()
_melee_hit = pygame.sprite.Group()
_key_sprites = pygame.sprite.Group()
_magic_hit_sprites = pygame.sprite.Group()
_char_effect_sprites = pygame.sprite.Group()

BOW_HIT = game_data.BOW_HIT
SWORD_HIT = game_data.SWORD_HIT


class GameState(Enum):
    LVL_MENU = auto()
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    WIN = auto()
    LOSE = auto()


class GameMap:
    def __init__(self, level):
        self._map = engine_loading.load_level(level)
        self.start_pos = self.generate_level(self._map)

    def generate_level(self, level):
        start_pos = 0, 0
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    engine_main.Tile(game_data.images['empty'], (x, y))
                elif level[y][x] == '#':
                    engine_main.Tile(game_data.images['wall'], (x, y), _tile_sprites, _impenetrable)
                elif level[y][x] == '_':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                elif level[y][x] == 'A':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                    Door(game_data.images['door_opened'], (x, y), _tile_sprites, _door_sprites)
                    start_pos = x, y
                elif level[y][x] == 'B':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                    Door(game_data.images['door_closed'], (x, y), _tile_sprites, _close_door_sprites)
                elif level[y][x] == '?':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                    Key((x, y), _tile_sprites, _map_items_sprites, _key_sprites)
                elif level[y][x] == '!':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                    Enemy((x, y), _character_sprites, _enemy_sprites)
                elif level[y][x] == 'R':
                    engine_main.Tile(game_data.images['floor'], (x, y), _tile_sprites)
                    MagicHit((x, y), _tile_sprites, _map_items_sprites, _magic_hit_sprites)
        return start_pos

    def draw(self, screen):
        _tile_sprites.draw(screen)
        _map_items_sprites.draw(screen)
        _character_sprites.draw(screen)


class LvlManager:
    def __init__(self, maps):
        self.levels = [0 for _ in range(len(maps))]
        self.maps = maps
        self.levels[0] = 1
        self.levels[1] = 0
        self.levels[2] = 0
        self.max_level = 0
        self.active_level = 0

    def __len__(self):
        return len(self.levels)

    def unlock_next(self):
        if self.max_level + 1 < len(self.levels) and self.active_level == self.max_level:
            self.max_level += 1
            self.levels[self.max_level] = 1
            return True
        if self.active_level < self.max_level:
            return True
        return False

    def is_free(self, number):
        return bool(self.levels[number - 1])

    def set_active_level(self, number):
        self.active_level = number - 1


class Player(engine_main.Creature):
    def __init__(self, pos, *groups):
        super().__init__(game_data.images['player'], pos, *groups)
        self.inventory = Inventory(['hand', RangeWeapon(game_data.images['bow'], self.pos, engine_main._item_sprites),
                                    MeleeWeapon(game_data.images['sword'], self.pos, engine_main._item_sprites)])
        self.char_state = GameState.PLAYING
        self.sword_cooldown = game_data.SWORD_COOLDOWN
        self.bow_cooldown = game_data.BOW_COOLDOWN
        self.close_hit_cooldown = game_data.CLOSE_HIT_COOLDOWN
        # self.magic_run_cooldown = game_data.MAGIC_RUN_COOLDOWN
        self.player_health_bar = ResourceBar((20, 520), game_data.images['health_bar'], self.durability)
        self.speed = game_data.MAIN_CHAR_SPEED
        self.effects = []
        self.magic_num = -3
        self.magic_pos = False
        self.inventory.update()

    def update_cooldowns(self):
        global BOW_HIT, SWORD_HIT
        if self.sword_cooldown >= game_data.SWORD_COOLDOWN:
            self.sword_cooldown = 0
        elif self.sword_cooldown != 0:
            self.sword_cooldown += 1
        if self.bow_cooldown >= game_data.BOW_COOLDOWN:
            self.bow_cooldown = 0
        elif self.bow_cooldown != 0:
            self.bow_cooldown += 1
        if self.close_hit_cooldown >= game_data.CLOSE_HIT_COOLDOWN:
            self.close_hit_cooldown = 0
        else:
            self.close_hit_cooldown += 1
        for effect in self.effects:
            if isinstance(effect, MagicHit):
                if effect.cooldown >= game_data.MAGIC_HIT_COOLDOWN:
                    self.speed = game_data.MAIN_CHAR_SPEED
                    effect.update_cooldown(0)
                    _char_effect_sprites.remove(effect)
                    self.effects.remove(effect)
                    BOW_HIT = game_data.BOW_HIT
                    SWORD_HIT = game_data.SWORD_HIT
                elif effect.cooldown != 0:
                    effect.update_cooldown(effect.cooldown + 1)
                    self.magic_run_bar.take_current_health(game_data.MAGIC_HIT_COOLDOWN - effect.cooldown)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.player_health_bar.take_current_health(self.durability)
        self.update_cooldowns()
        self.update_image(0 if self.pos[0] <= pygame.mouse.get_pos()[0] / 50 else 1)
        self.rect = self.rect.move(self.vx / game_data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -3 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / game_data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, self.vy / abs(self.vy) * -3 if self.vy else 0)
        if pygame.sprite.spritecollideany(self, _bullet_sprites) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _bullet_sprites).kill()
            self.durability -= BOW_HIT
        if pygame.sprite.spritecollideany(self, _enemy_sprites) and self.close_hit_cooldown == 0:
            self.durability -= 3
            game_data.char_hit_sound.play()
        if self.durability <= 0:
            self.durability = 0
            self.char_state = GameState.LOSE
            game_data.playing_music.stop()
            pygame.mixer.Channel(0).play(game_data.lose_music)

    def init_health_bar(self):
        pass

    def get_state(self):
        return self.char_state

    def attack(self):
        global SWORD_HIT, BOW_HIT
        equipped = self.inventory.equipped()
        if equipped and isinstance(equipped, Tool):
            if isinstance(equipped, RangeWeapon) and self.bow_cooldown == 0:
                equipped.shoot(engine_math.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                           / 50, pygame.mouse.get_pos()[1] / 50))
                self.bow_cooldown += 1
                game_data.bow_shoot_sound.play()
            elif isinstance(equipped, MeleeWeapon) and self.sword_cooldown == 0:
                equipped.hit(engine_math.calculate_angle(*self.pos, pygame.mouse.get_pos()[0]
                                                         / 50, pygame.mouse.get_pos()[1] / 50))
                self.sword_cooldown += 1
                game_data.sword_hit_sound.play()
        elif equipped and isinstance(equipped, Magic):
            if isinstance(equipped, MagicHit):
                equipped.activate()
                self.effects.append(equipped)
                del self.inventory.storage[self.inventory.get_index()]
                self.inventory.active_position -= 1 if self.inventory.active_position \
                                                       == len(self.inventory) else 0
                self.inventory.update()
                self.inventory.take_active_tool(self.inventory.active_position)
                BOW_HIT = 999
                SWORD_HIT = 999
                equipped.update_cooldown(1)
                self.magic_run_bar = ResourceBar((20, 555), game_data.images['resource_bar'],
                                                 game_data.MAGIC_HIT_COOLDOWN)
                game_data.take_item_sound.play()
        elif equipped == 'hand':
            if pygame.sprite.spritecollideany(self, _key_sprites):
                pygame.sprite.spritecollideany(self, _key_sprites).kill()
                self.inventory.add_item(Key(self.pos, engine_main._item_sprites))
                game_data.take_item_sound.play()
            elif pygame.sprite.spritecollideany(self, _magic_hit_sprites):
                pygame.sprite.spritecollideany(self, _magic_hit_sprites).kill()
                self.inventory.add_item(MagicHit(self.pos, engine_main._item_sprites))
                game_data.take_item_sound.play()
        elif pygame.sprite.spritecollideany(self, _close_door_sprites) and isinstance(equipped, Key):
            _close_door_sprites.update(activate=True)
            _equipped_item_sprites.remove(self.inventory.equipped())
            del self.inventory.storage[self.inventory.get_index()]
            # _icon_tool_interface_sprites.update(position=self.inventory.get_index())
            self.inventory.active_position -= 1 if self.inventory.active_position\
                                                   == len(self.inventory) else 0
            self.inventory.update()
            self.inventory.take_active_tool(self.inventory.active_position)
        self.inventory.update()

    def move(self, event):
        if event.key == pygame.K_w:
            self.vy -= game_data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_a:
            self.vx -= game_data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_s:
            self.vy += game_data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)
        if event.key == pygame.K_d:
            self.vx += game_data.MAIN_CHAR_SPEED * (1 if event.type == pygame.KEYDOWN else -1)

    def update_pos(self):
        global PLAYER_POS
        self.pos = self.x, self.y = self.rect.x / game_data.TITLE_WIDTH, self.rect.y / game_data.TITLE_HEIGHT
        PLAYER_POS = self.pos[:]
        self.inventory.update_tools_pos(self.x, self.y, self.rect)
        for effect in self.effects:
            effect.update_pos(self.x, self.y)

    def change_equipped(self, event):
        self.inventory.update()
        if event.type in (pygame.KEYUP, pygame.KEYDOWN):
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
        else:
            position = (self.inventory.get_index()
                        + (1 if event.button == pygame.BUTTON_WHEELDOWN else -1)) % len(self.inventory)
        self.inventory.take_active_tool(position)
        self.inventory.update()


class Enemy(engine_main.Creature):
    def __init__(self, pos, *groups):
        super().__init__(game_data.images['enemy'], pos, *groups)
        self.is_active = False

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / game_data.FPS, 0)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(self.vx / abs(self.vx) * -2 if self.vx else 0, 0)
        self.rect = self.rect.move(0, self.vy / game_data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable):
            self.rect = self.rect.move(0, int(self.vy / abs(self.vy) * -2 if self.vy else 0))
        if pygame.sprite.spritecollideany(self, _bullet_sprites) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _bullet_sprites).kill()
            self.durability -= BOW_HIT
        if pygame.sprite.spritecollideany(self, _melee_hit) and _enemy_sprites.has(self):
            pygame.sprite.spritecollideany(self, _melee_hit).kill()
            self.durability -= SWORD_HIT
        if self.durability <= 0:
            game_data.enemy_hit_sound.play()
            self.kill()

    def move(self):
        if 0.5 <= self.target_distance(PLAYER_POS) <= 3 or self.is_active:
            self.is_active = True
            if not (self.is_active and 0.5 <= self.target_distance(PLAYER_POS) <= 5):
                self.is_active = False
            if not PLAYER_POS[0] - 0.05 <= self.x <= PLAYER_POS[0] + 0.05:
                if self.x < PLAYER_POS[0]:
                    self.vx = game_data.NPC_SPEED
                if self.x > PLAYER_POS[0]:
                    self.vx = -game_data.NPC_SPEED
            else:
                self.vx = 0
            if not PLAYER_POS[1] - 0.05 <= self.y <= PLAYER_POS[1] + 0.05:
                if self.y < PLAYER_POS[1]:
                    self.vy = game_data.NPC_SPEED
                if self.y > PLAYER_POS[1]:
                    self.vy = -game_data.NPC_SPEED
            else:
                self.vy = 0
        else:
            self.vx = 0
            self.vy = 0

    def target_distance(self, pos):
        n = engine_math.hypotenuse(*self.pos, *pos)
        return n


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_img, pos, angle, *groups, not_bullet=False):
        super().__init__(engine_main._all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.is_not_bullet = not_bullet
        self.vx, self.vy = engine_math.change_position(engine_math.calculate_angle(pos[0] * game_data.TITLE_WIDTH,
                                                                                   pos[1] * game_data.TITLE_HEIGHT,
                                                                                   *pygame.mouse.get_pos()),
                                                       game_data.BULLET_SPEED, 1)
        self.angle = angle
        if _melee_hit in groups:
            self.durability = 3
        elif _non_attack_bullet_sprites in groups:
            self.durability = 2
        else:
            self.durability = 10
        self._init_sprite(sprite_img)

    def _init_sprite(self, sprite_img):
        self.image = sprite_img
        self.rect = self.image.get_rect().move(game_data.TITLE_SIZE[0] * self.x,
                                               game_data.TITLE_SIZE[1] * self.y)
        self.image, self.rect = self.rotate(self.image, self.rect, self.angle)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        if self.is_not_bullet:
            self.durability -= 1
        self.rect = self.rect.move(self.vx / game_data.FPS, self.vy / game_data.FPS)
        if pygame.sprite.spritecollideany(self, _impenetrable) or self.durability <= 0:
            self.kill()

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, -angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def update_pos(self, x, y):
        self.rect = self.image.get_rect().move(x * game_data.TITLE_WIDTH, y * game_data.TITLE_HEIGHT)
        self.pos = self.x, self.y = self.rect.x / game_data.TITLE_WIDTH, self.rect.y / game_data.TITLE_HEIGHT


class Inventory:
    def __init__(self, items):
        self.storage = [*items]
        self.active_position = 0

    def update(self):
        _icon_tool_interface_sprites.update(kill=True)
        _icon_tool_interface_sprites.add(ItemIcon((175 + self.active_position * 60, 515), 0, 'outline'))
        for index, tool in enumerate(self.storage):
            if tool == 'hand':
                _icon_tool_interface_sprites.add(ItemIcon((180 + index * 60, 520), index, 'hand'))
            elif isinstance(tool, RangeWeapon):
                _icon_tool_interface_sprites.add(ItemIcon((180 + index * 60, 520), index, 'bow'))
            elif isinstance(tool, MeleeWeapon):
                _icon_tool_interface_sprites.add(ItemIcon((180 + index * 60, 520), index, 'sword'))
            elif isinstance(tool, Key):
                _icon_tool_interface_sprites.add(ItemIcon((180 + index * 60, 520), index, 'key'))
            elif isinstance(tool, MagicHit):
                _icon_tool_interface_sprites.add(ItemIcon((180 + index * 60, 520), index, 'magic_hit_item'))

    def take_active_tool(self, position):
        if isinstance(self.storage[self.active_position if self.active_position
                                                           + 1 <= len(self.storage) else 0], engine_main.Item):
            _equipped_item_sprites.remove(self.storage[self.active_position if self.active_position
                                                                               + 1 <= len(self.storage) else 0])
        self.active_position = position if position + 1 <= len(self.storage) else 0
        if isinstance(self.storage[self.active_position if self.active_position
                                                           + 1 <= len(self.storage) else 0], engine_main.Item):
            if isinstance(self.storage[self.active_position], Magic):
                # _char_effect_sprites.add(self.storage[self.active_position])
                pass
            else:
                _equipped_item_sprites.add(self.storage[self.active_position])

    def add_item(self, item):
        self.storage.append(item)

    def get_index(self):
        return self.active_position

    def __len__(self):
        return len(self.storage)

    def equipped(self):
        return self.storage[self.active_position if self.active_position
                                                    + 1 <= len(self.storage) else 0] if self.storage else None

    def update_tools_pos(self, x, y, rect):
        for tool in self.storage:
            if isinstance(tool, engine_main.Item):
                tool.update_pos(x + (rect.width - tool.rect.width) // 2 /
                                game_data.TITLE_WIDTH, y + 5 / game_data.TITLE_HEIGHT)


class ItemIcon(pygame.sprite.Sprite):
    def __init__(self, pos, inventory_position, sprite_type, *groups):
        super().__init__(engine_main._all_sprites, engine_main._interface_sprites,
                         _icon_tool_interface_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.inventory_position = inventory_position
        self.image = game_data.images[sprite_type]
        if sprite_type == 'bow':
            self.image = pygame.transform.rotate(self.image, -45)
            self.image = pygame.transform.scale(self.image, (45, 45))
        elif sprite_type != 'outline':
            self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *events, kill=False, position=777):
        if kill:
            self.kill()
        if position <= self.inventory_position:
            self.kill()
        self.rect = self.image.get_rect().move(self.x, self.y)


class ResourceBar(engine_main.Interface):
    def __init__(self, pos, sprite_img, health):
        super().__init__(pos, sprite_img, _bar_sprites)
        self.max_health = self.health = health
        self.image = pygame.transform.scale(self.image, (150, 25))
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.image = pygame.transform.scale(self.image, (150 * self.health // self.max_health, 25))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect().move(self.x, self.y)

    def take_current_health(self, health):
        self.health = health if health > 0 else 0


class SkillBar(engine_main.Interface):
    pass


class Key(engine_main.Item):
    def __init__(self, pos, *groups):
        super().__init__(game_data.images['key'], pos, *groups)
        self.pos = self.x, self.y = pos


class Magic(engine_main.Item):
    pass


class MagicHit(Magic):
    def __init__(self, pos, *groups):
        super().__init__(game_data.images['magic_hit_item'], pos, *groups)
        self.pos = self.x, self.y = pos
        self.cooldown = game_data.MAGIC_HIT_COOLDOWN

    def activate(self):
        self.image = game_data.images['magic_hit_ef']
        _char_effect_sprites.add(self)

    def update_cooldown(self, num):
        self.cooldown = num


class Tool(engine_main.Item):
    pass


class RangeWeapon(Tool):
    def shoot(self, angle):
        Bullet(game_data.images['arrow'],
               (self.x + 15 / game_data.TITLE_WIDTH, self.y + 11 / game_data.TITLE_HEIGHT), angle, _bullet_sprites)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / game_data.FPS, self.vy / game_data.FPS)
        angle = engine_math.calculate_angle(self.x * game_data.TITLE_WIDTH,
                                            self.y * game_data.TITLE_HEIGHT, *pygame.mouse.get_pos())
        self.image, self.rect = self.rotate(self.orig_image, self.rect, angle)


class MeleeWeapon(Tool):
    def hit(self, look_target):
        Bullet(game_data.images['arrow'],
               (self.x + 15 / game_data.TITLE_WIDTH, self.y + 11 / game_data.TITLE_HEIGHT),
               look_target, _melee_hit, not_bullet=True)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.update_image(0 if PLAYER_POS[0] <= pygame.mouse.get_pos()[0] / 50 else 1)

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


class Door(engine_main.Tile):
    def __init__(self, sprite_img, pos, *groups):
        super().__init__(sprite_img, pos, *groups)
        self.durability = 2

    def update(self, *events, kill=False, activate=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / game_data.FPS, self.vy / game_data.FPS)
        if activate:
            self.durability -= 1
        if self.durability == 0:
            self.kill()
