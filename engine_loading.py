import os
import sys
import pygame
import game_data


def load_image(name, color_key=None):
    fullname = os.path.join(game_data.DATA_PATH, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if color_key is not None:
    #     image = image.convert()
    #     if color_key == -1:
    #         color_key = image.get_at((0, 0))
    #     image.set_colorkey(color_key)
    # else:
    #     image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join(game_data.MAP_PATH, filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
