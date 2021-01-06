import pygame

from loading import load_image


FPS = 60
RESOLUTION = WIDTH, HEIGHT = 800, 600
MAIN_CHAR_SPEED = 20
NPC_SPEED = 18
DATA_PATH = 'textures'
tile_size = tile_width, tile_height = 50, 50

images = {'player': pygame.transform.scale(load_image('character.png'), tile_size)}
