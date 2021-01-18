import pygame
import loading


FPS = 60
RESOLUTION = WIDTH, HEIGHT = 800, 600
MAIN_CHAR_SPEED = 200
NPC_SPEED = 60
BULLET_SPEED = 500
hp = 34
DATA_PATH = 'textures'
MAP_PATH = 'maps'
tile_size = tile_width, tile_height = 50, 50

images = {'player': pygame.transform.scale(loading.load_image('character.png'), (tile_width - 5, tile_height - 5)),
          'arrow': pygame.transform.scale(loading.load_image('arrow.png'), (9, 28)),
          'bow': pygame.transform.scale(loading.load_image('bow.png'), (40, 15)),
          'sword': pygame.transform.scale(loading.load_image('sword.png'), (30, 30)),
          'empty': pygame.transform.scale(loading.load_image('empty.png'), tile_size),
          'wall': pygame.transform.scale(loading.load_image('wall.png'), tile_size),
          'floor': pygame.transform.scale(loading.load_image('floor.png'), tile_size),
          'enemy': pygame.transform.scale(loading.load_image('enemy.gif'), (tile_width - 5, tile_height - 5)),
          'key': pygame.transform.scale(loading.load_image('key.png'), (40, 40)),
          'door_closed': pygame.transform.scale(loading.load_image('door_closed.png'), tile_size),
          'door_opened': pygame.transform.scale(loading.load_image('door_opened.png'), tile_size),
          'b_start_game': pygame.transform.scale(loading.load_image('b_start_game.png'), (100, 50)),
          'b_exit': pygame.transform.scale(loading.load_image('b_exit.png'), (100, 50)),
          'b_continue': pygame.transform.scale(loading.load_image('b_continue.png'), (100, 50)),
          'b_back_to_menu': pygame.transform.scale(loading.load_image('b_back_to_menu.png'), (100, 50))}

pygame.mixer.init()
main_menu_music = pygame.mixer.Sound('sounds\menu.mp3')
playing_music = pygame.mixer.Sound('sounds\playing.mp3')
