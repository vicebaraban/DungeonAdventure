import os
import pygame
import engine_loading


FPS = 60
RESOLUTION = 800, 600
MAIN_CHAR_SPEED = 200
NPC_SPEED = 120
BULLET_SPEED = 500
HP = 34
BOW_HIT = 7
SWORD_HIT = 17
BOW_COOLDOWN = 40
SWORD_COOLDOWN = 60
CLOSE_HIT_COOLDOWN = 35
MAGIC_HIT_COOLDOWN = 1000
DATA_PATH = 'textures'
MAP_PATH = 'maps'
SOUND_PATH = 'sounds'
TITLE_SIZE = TITLE_WIDTH, TITLE_HEIGHT = 50, 50

maps = ['map1.txt', 'map2.txt', 'map3.txt']

images = {'player': pygame.transform.scale(engine_loading.load_image('character.png'), (TITLE_WIDTH - 6, TITLE_HEIGHT - 6)),
          'arrow': pygame.transform.scale(engine_loading.load_image('arrow.png'), (9, 28)),
          'bow': pygame.transform.scale(engine_loading.load_image('bow.png'), (40, 15)),
          'sword': pygame.transform.scale(engine_loading.load_image('sword.png'), (30, 30)),
          'empty': pygame.transform.scale(engine_loading.load_image('empty.png'), TITLE_SIZE),
          'wall': pygame.transform.scale(engine_loading.load_image('wall.png'), TITLE_SIZE),
          'floor': pygame.transform.scale(engine_loading.load_image('floor.png'), TITLE_SIZE),
          'enemy': pygame.transform.scale(engine_loading.load_image('enemy.gif'), (TITLE_WIDTH - 10, TITLE_HEIGHT - 10)),
          'key': pygame.transform.scale(engine_loading.load_image('key.png'), (40, 40)),
          'magic_hit_item': pygame.transform.scale(engine_loading.load_image('magic_hit_item.png'), (40, 40)),
          'magic_hit_ef': pygame.transform.scale(engine_loading.load_image('magic_hit_ef.png'), (44, 44)),
          'hand': pygame.transform.scale(engine_loading.load_image('hand.png'), TITLE_SIZE),
          'door_closed': pygame.transform.scale(engine_loading.load_image('door_closed.png'), TITLE_SIZE),
          'door_opened': pygame.transform.scale(engine_loading.load_image('door_opened.png'), TITLE_SIZE),
          'b_start_game': pygame.transform.scale(engine_loading.load_image('b_start_game.png'), (100, 50)),
          'b_exit': pygame.transform.scale(engine_loading.load_image('b_exit.png'), (100, 50)),
          'b_continue': pygame.transform.scale(engine_loading.load_image('b_continue.png'), (100, 50)),
          'b_back_to_menu': pygame.transform.scale(engine_loading.load_image('b_back_to_menu.png'), (100, 50)),
          'b_level_menu': pygame.transform.scale(engine_loading.load_image('b_level_menu.png'), (100, 50)),
          'b_level_1': pygame.transform.scale(engine_loading.load_image('b_level_1.png'), (100, 50)),
          'b_level_2': pygame.transform.scale(engine_loading.load_image('b_level_2.png'), (100, 50)),
          'b_level_3': pygame.transform.scale(engine_loading.load_image('b_level_3.png'), (100, 50)),
          'b_level_4': pygame.transform.scale(engine_loading.load_image('b_level_4.png'), (100, 50)),
          'b_level_5': pygame.transform.scale(engine_loading.load_image('b_level_5.png'), (100, 50)),
          'b_level_6': pygame.transform.scale(engine_loading.load_image('b_level_6.png'), (100, 50)),
          'b_level_7': pygame.transform.scale(engine_loading.load_image('b_level_7.png'), (100, 50)),
          'b_level_8': pygame.transform.scale(engine_loading.load_image('b_level_8.png'), (100, 50)),
          'b_level_9': pygame.transform.scale(engine_loading.load_image('b_level_9.png'), (100, 50)),
          'b_next_level': pygame.transform.scale(engine_loading.load_image('b_next_level.png'), (100, 50)),
          'b_retry_level': pygame.transform.scale(engine_loading.load_image('b_retry_level.png'), (100, 50)),
          'lvl_active': pygame.transform.scale(engine_loading.load_image('lvl_active.png'), (100, 50)),
          'lvl_max': pygame.transform.scale(engine_loading.load_image('lvl_max.png'), (100, 50)),
          'menu_background': pygame.transform.scale(engine_loading.load_image('menu_background.png'), (800, 600)),
          'pause_background': pygame.transform.scale(engine_loading.load_image('pause_background.png'), (800, 600)),
          'victory_background': pygame.transform.scale(engine_loading.load_image('victory_background.png'), (800, 600)),
          'lose_background': pygame.transform.scale(engine_loading.load_image('lose_background.png'), (800, 600)),
          'level_menu_background': pygame.transform.scale(engine_loading.load_image('level_menu_background.png'), (800, 600)),
          'cursor': pygame.transform.scale(engine_loading.load_image('cursor.png'), (30, 30)),
          'health_bar': engine_loading.load_image('health_bar.png'),
          'resource_bar': engine_loading.load_image('resource_bar.png'),
          'playing_ui': engine_loading.load_image('playing_ui.png'),
          'outline': engine_loading.load_image('outline.png')}

pygame.mixer.init()
main_menu_music = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'menu.wav'))
playing_music = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'playing.wav'))
victory_music = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'ivictory.wav'))
lose_music = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'lose.wav'))
bow_shoot_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'ibow_shoot.wav'))
sword_hit_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'sword_hit.wav'))
char_hit_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'char_hit.wav'))
enemy_hit_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'enemy_hit.wav'))
take_item_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'itake_item.wav'))
#
# player = pygame.transform.scale(engine_loading.load_image('character.png'), (TITLE_WIDTH - 6, TITLE_HEIGHT - 6)),
# arrow = pygame.transform.scale(engine_loading.load_image('arrow.png'), (9, 28)),
# bow = pygame.transform.scale(engine_loading.load_image('bow.png'), (40, 15)),
# sword = pygame.transform.scale(engine_loading.load_image('sword.png'), (30, 30)),
# empty = pygame.transform.scale(engine_loading.load_image('empty.png'), TITLE_SIZE),
# wall = pygame.transform.scale(engine_loading.load_image('wall.png'), TITLE_SIZE),
# floor = pygame.transform.scale(engine_loading.load_image('floor.png'), TITLE_SIZE),
# enemy = pygame.transform.scale(engine_loading.load_image('enemy.gif'), (TITLE_WIDTH - 10, TITLE_HEIGHT - 10)),
# key = pygame.transform.scale(engine_loading.load_image('magic_run_item.png'), (40, 40)),
# hand = pygame.transform.scale(engine_loading.load_image('hand.png'), TITLE_SIZE),
# door_closed = pygame.transform.scale(engine_loading.load_image('door_closed.png'), TITLE_SIZE),
# door_opened = pygame.transform.scale(engine_loading.load_image('door_opened.png'), TITLE_SIZE),
# b_start_game = pygame.transform.scale(engine_loading.load_image('b_start_game.png'), (100, 50)),
# b_exit = pygame.transform.scale(engine_loading.load_image('b_exit.png'), (100, 50)),
# b_continue = pygame.transform.scale(engine_loading.load_image('b_continue.png'), (100, 50)),
# b_back_to_menu = pygame.transform.scale(engine_loading.load_image('b_back_to_menu.png'), (100, 50)),
# b_level_menu = pygame.transform.scale(engine_loading.load_image('b_level_menu.png'), (100, 50)),
# b_level_1 = pygame.transform.scale(engine_loading.load_image('b_level_1.png'), (100, 50)),
# b_level_2 = pygame.transform.scale(engine_loading.load_image('b_level_2.png'), (100, 50)),
# b_level_3 = pygame.transform.scale(engine_loading.load_image('b_level_3.png'), (100, 50)),
# b_level_4 = pygame.transform.scale(engine_loading.load_image('b_level_4.png'), (100, 50)),
# b_level_5 = pygame.transform.scale(engine_loading.load_image('b_level_5.png'), (100, 50)),
# b_level_6 = pygame.transform.scale(engine_loading.load_image('b_level_6.png'), (100, 50)),
# b_level_7 = pygame.transform.scale(engine_loading.load_image('b_level_7.png'), (100, 50)),
# b_level_8 = pygame.transform.scale(engine_loading.load_image('b_level_8.png'), (100, 50)),
# b_level_9 = pygame.transform.scale(engine_loading.load_image('b_level_9.png'), (100, 50)),
# b_next_level = pygame.transform.scale(engine_loading.load_image('b_next_level.png'), (100, 50)),
# b_retry_level = pygame.transform.scale(engine_loading.load_image('b_retry_level.png'), (100, 50)),
# lvl_active = pygame.transform.scale(engine_loading.load_image('lvl_active.png'), (100, 50)),
# lvl_max = pygame.transform.scale(engine_loading.load_image('lvl_max.png'), (100, 50)),
# menu_background = pygame.transform.scale(engine_loading.load_image('menu_background.png'), (800, 600)),
# pause_background = pygame.transform.scale(engine_loading.load_image('pause_background.png'), (800, 600)),
# victory_background = pygame.transform.scale(engine_loading.load_image('victory_background.png'), (800, 600)),
# lose_background = pygame.transform.scale(engine_loading.load_image('lose_background.png'), (800, 600)),
# level_menu_background = pygame.transform.scale(engine_loading.load_image('level_menu_background.png'), (800, 600)),
# cursor = pygame.transform.scale(engine_loading.load_image('cursor.png'), (30, 30)),
# health_bar = engine_loading.load_image('health_bar.png'),
# playing_ui = engine_loading.load_image('playing_ui.png'),
# outline = engine_loading.load_image('outline.png')
#
# class Data:
#     def __init__(self):
#         self.fps = 60
#         self.resolution = 800, 600
#         self.main_char_speed = 200
#         self.npc_speed = 120
#         self.bullet_speed = 500
#         self.hp = 34
#         self.bow_cooldown = 40
#         self.sword_cooldown = 60
#         self.close_hit_cooldown = 35
#         self.data_path = 'textures'
#         self.map_path = 'maps'
#         self.sound_path = 'sounds'
#         self.title_size = title_width, title_height = 50, 50
#
#         self.maps = ['map1.txt', 'map2.txt', 'map3.txt']
#
#         self.player = pygame.transform.scale(engine_loading.load_image('character.png'), (title_width - 6, title_height - 6))
#         self.arrow = pygame.transform.scale(engine_loading.load_image('arrow.png'), (9, 28))
#         self.bow = pygame.transform.scale(engine_loading.load_image('bow.png'), (40, 15))
#         self.sword = pygame.transform.scale(engine_loading.load_image('sword.png'), (30, 30))
#         self.empty = pygame.transform.scale(engine_loading.load_image('empty.png'), self.title_size)
#         self.wall = pygame.transform.scale(engine_loading.load_image('wall.png'), self.title_size)
#         self.floor = pygame.transform.scale(engine_loading.load_image('floor.png'), self.title_size)
#         self.enemy = pygame.transform.scale(engine_loading.load_image('enemy.gif'), (title_width - 10, title_height - 10))
#         self.key = pygame.transform.scale(engine_loading.load_image('magic_run_item.png'), (40, 40))
#         self.hand = pygame.transform.scale(engine_loading.load_image('hand.png'), self.title_size)
#         self.door_closed = pygame.transform.scale(engine_loading.load_image('door_closed.png'), self.title_size)
#         self.door_opened = pygame.transform.scale(engine_loading.load_image('door_opened.png'), self.title_size)
#         self.b_start_game = pygame.transform.scale(engine_loading.load_image('b_start_game.png'), (100, 50))
#         self.b_exit = pygame.transform.scale(engine_loading.load_image('b_exit.png'), (100, 50))
#         self.b_continue = pygame.transform.scale(engine_loading.load_image('b_continue.png'), (100, 50))
#         self.b_back_to_menu = pygame.transform.scale(engine_loading.load_image('b_back_to_menu.png'), (100, 50))
#         self.b_level_menu = pygame.transform.scale(engine_loading.load_image('b_level_menu.png'), (100, 50))
#         self.b_level_1 = pygame.transform.scale(engine_loading.load_image('b_level_1.png'), (100, 50))
#         self.b_level_2 = pygame.transform.scale(engine_loading.load_image('b_level_2.png'), (100, 50))
#         self.b_level_3 = pygame.transform.scale(engine_loading.load_image('b_level_3.png'), (100, 50))
#         self.b_level_4 = pygame.transform.scale(engine_loading.load_image('b_level_4.png'), (100, 50))
#         self.b_level_5 = pygame.transform.scale(engine_loading.load_image('b_level_5.png'), (100, 50))
#         self.b_level_6 = pygame.transform.scale(engine_loading.load_image('b_level_6.png'), (100, 50))
#         self.b_level_7 = pygame.transform.scale(engine_loading.load_image('b_level_7.png'), (100, 50))
#         self.b_level_8 = pygame.transform.scale(engine_loading.load_image('b_level_8.png'), (100, 50))
#         self.b_level_9 = pygame.transform.scale(engine_loading.load_image('b_level_9.png'), (100, 50))
#         self.b_next_level = pygame.transform.scale(engine_loading.load_image('b_next_level.png'), (100, 50))
#         self.b_retry_level = pygame.transform.scale(engine_loading.load_image('b_retry_level.png'), (100, 50))
#         self.lvl_active = pygame.transform.scale(engine_loading.load_image('lvl_active.png'), (100, 50))
#         self.lvl_max = pygame.transform.scale(engine_loading.load_image('lvl_max.png'), (100, 50))
#         self.menu_background = pygame.transform.scale(engine_loading.load_image('menu_background.png'), (800, 600))
#         self.pause_background = pygame.transform.scale(engine_loading.load_image('pause_background.png'), (800, 600))
#         self.victory_background = pygame.transform.scale(engine_loading.load_image('victory_background.png'), (800, 600))
#         self.lose_background = pygame.transform.scale(engine_loading.load_image('lose_background.png'), (800, 600))
#         self.level_menu_background = pygame.transform.scale(engine_loading.load_image('level_menu_background.png'), (800, 600))
#         self.cursor = pygame.transform.scale(engine_loading.load_image('cursor.png'), (30, 30))
#         self.health_bar = engine_loading.load_image('health_bar.png')
#         self.playing_ui = engine_loading.load_image('playing_ui.png')
#         self.outline = engine_loading.load_image('outline.png')
#
