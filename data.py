import pygame
import loading


FPS = 60
RESOLUTION = WIDTH, HEIGHT = 800, 600
MAIN_CHAR_SPEED = 200
NPC_SPEED = 120
BULLET_SPEED = 500
BULLET_TIME = 10
DATA_PATH = 'textures'
MAP_PATH = 'maps'
tile_size = tile_width, tile_height = 50, 50

images = {'player': pygame.transform.scale(loading.load_image('character.png'), (tile_width - 5, tile_height - 5)),
          'arrow': pygame.transform.scale(loading.load_image('arrow.png'), (8, 10)),
          'bow': pygame.transform.scale(loading.load_image('bow.png'), (10, 30)),
          'sword': pygame.transform.scale(loading.load_image('sword.png'), (30, 30)),
          'button': pygame.transform.scale(loading.load_image('button.png'), (30, 30)),
          'empty': pygame.transform.scale(loading.load_image('empty.png'), tile_size),
          'wall': pygame.transform.scale(loading.load_image('wall.png'), tile_size),
          'floor': pygame.transform.scale(loading.load_image('floor.png'), tile_size)}
