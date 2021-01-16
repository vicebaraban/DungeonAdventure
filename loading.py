import os
import sys
import pygame
import data
import engine


def load_image(name, color_key=None):
    fullname = os.path.join(data.DATA_PATH, name)
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
    filename = data.MAP_PATH + '/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    start_pos = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                engine.Tile('empty', (x, y))
            elif level[y][x] == '#':
                engine.Tile('wall', (x, y), engine._tile_sprites, engine._impenetrable)
            elif level[y][x] == '_':
                engine.Tile('floor', (x, y), engine._tile_sprites)
            elif level[y][x] == 'A':
                engine.Tile('floor', (x, y), engine._tile_sprites)
                engine.Door(True, (x, y), engine._tile_sprites, engine._door_sprites)
                start_pos = x, y
            elif level[y][x] == 'B':
                engine.Tile('floor', (x, y), engine._tile_sprites)
                engine.Door(False, (x, y), engine._tile_sprites, engine._door_sprites)
            elif level[y][x] == '?':
                engine.Tile('floor', (x, y), engine._tile_sprites)
                engine.Key((x, y), engine._tile_sprites, engine._map_items_sprites)
            elif level[y][x] == '!':
                engine.Tile('floor', (x, y), engine._tile_sprites)
                engine.Enemy((x, y), engine._character_sprites, engine._enemy_sprites)
    return start_pos