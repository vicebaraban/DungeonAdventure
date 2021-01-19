import os
import pygame
import loading


FPS = 60
RESOLUTION = WIDTH, HEIGHT = 800, 600
MAIN_CHAR_SPEED = 200
NPC_SPEED = 120
BULLET_SPEED = 500
HP = 34
BOW_COOLDOWN = 40
SWORD_COOLDOWN = 60
CLOSE_HIT_COOLDOWN = 35
DATA_PATH = 'textures'
MAP_PATH = 'maps'
SOUND_PATH = 'sounds'
TITLE_SIZE = TITLE_WIDTH, TITLE_HEIGHT = 50, 50

images = {'player': pygame.transform.scale(loading.load_image('character.png'), (TITLE_WIDTH - 5, TITLE_HEIGHT - 5)),
          'arrow': pygame.transform.scale(loading.load_image('arrow.png'), (9, 28)),
          'bow': pygame.transform.scale(loading.load_image('bow.png'), (40, 15)),
          'sword': pygame.transform.scale(loading.load_image('sword.png'), (30, 30)),
          'empty': pygame.transform.scale(loading.load_image('empty.png'), TITLE_SIZE),
          'wall': pygame.transform.scale(loading.load_image('wall.png'), TITLE_SIZE),
          'floor': pygame.transform.scale(loading.load_image('floor.png'), TITLE_SIZE),
          'enemy': pygame.transform.scale(loading.load_image('enemy.gif'), (TITLE_WIDTH - 5, TITLE_HEIGHT - 5)),
          'key': pygame.transform.scale(loading.load_image('key.png'), (40, 40)),
          'door_closed': pygame.transform.scale(loading.load_image('door_closed.png'), TITLE_SIZE),
          'door_opened': pygame.transform.scale(loading.load_image('door_opened.png'), TITLE_SIZE),
          'b_start_game': pygame.transform.scale(loading.load_image('b_start_game.png'), (100, 50)),
          'b_exit': pygame.transform.scale(loading.load_image('b_exit.png'), (100, 50)),
          'b_continue': pygame.transform.scale(loading.load_image('b_continue.png'), (100, 50)),
          'b_back_to_menu': pygame.transform.scale(loading.load_image('b_back_to_menu.png'), (100, 50)),
          'menu_background': pygame.transform.scale(loading.load_image('menu_background.png'), (800, 600)),
          'pause_background': pygame.transform.scale(loading.load_image('pause_background.png'), (800, 600)),
          'victory_background': pygame.transform.scale(loading.load_image('victory_background.png'), (800, 600)),
          'lose_background': pygame.transform.scale(loading.load_image('lose_background.png'), (800, 600)),
          'cursor': pygame.transform.scale(loading.load_image('cursor.png'), (30, 30))}

pygame.mixer.init()
main_menu_music = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'menu.ogg'))
playing_music = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'playing.ogg'))
victory_music = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'ivictory.ogg'))
lose_music = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'lose.ogg'))
bow_shoot_sound = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'ibow_shoot.ogg'))
sword_hit_sound = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'sword_hit.ogg'))
char_hit_sound = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'char_hit.ogg'))
enemy_hit_sound = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'enemy_hit.ogg'))
take_item_sound = pygame.mixer.Sound(os.path.join('data', SOUND_PATH, 'itake_item.ogg'))
