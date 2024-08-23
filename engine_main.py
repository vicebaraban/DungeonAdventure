import pygame


_all_sprites = pygame.sprite.Group()
_interface_sprites = pygame.sprite.Group()
_item_sprites = pygame.sprite.Group()

RESOLUTION = 800, 600
TITLE_SIZE = TITLE_WIDTH, TITLE_HEIGHT = 50, 50
FPS = 60
DURABILITY = 34


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_img, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.x1, self.x2, self.y1, self.y2 = pos[0], pos[0] + 2, pos[1], pos[1] + 1
        self._init_sprite(sprite_img)

    def _init_sprite(self, sprite_img):
        self.image = sprite_img
        self.rect = self.image.get_rect().move(TITLE_WIDTH * self.x1, TITLE_HEIGHT * self.y1)

    def is_clicked(self):
        mouse_x = pygame.mouse.get_pos()[0] / TITLE_HEIGHT
        mouse_y = pygame.mouse.get_pos()[1] / TITLE_WIDTH
        if self.x1 <= mouse_x <= self.x2 and self.y1 <= mouse_y <= self.y2:
            return True
        return False

    def update(self, kill=False):
        if kill:
            self.kill()


class Creature(pygame.sprite.Sprite):
    def __init__(self, sprite_img, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.angle = 0
        self._init_sprite(sprite_img)

    def _init_sprite(self, sprite_img):
        self.orig_image = sprite_img
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(TITLE_SIZE[0] * self.x,
                                               TITLE_SIZE[1] * self.y)
        self.vx, self.vy = 0, 0
        self.durability = DURABILITY

    def update(self, *events, kill=False):
        if kill:
            self.kill()

    def update_image(self, direction):
        if direction == 1:
            self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image

    def update_pos(self):
        self.pos = self.x, self.y = self.rect.x / TITLE_WIDTH, self.rect.y / TITLE_HEIGHT


class Interface(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_img, *groups):
        super().__init__(_all_sprites, _interface_sprites, *groups)
        self.pos = self.x, self.y = pos
        self.image = sprite_img
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.image.get_rect().move(self.x, self.y)


class Item(pygame.sprite.Sprite):
    def __init__(self, sprite_img, pos, *groups):
        super().__init__(_all_sprites, _item_sprites, *groups)
        self.pos = self.x, self.y = pos
        self._init_sprite(sprite_img)

    def _init_sprite(self, sprite_img):
        self.orig_image = sprite_img
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(TITLE_SIZE[0] * self.x,
                                               TITLE_SIZE[1] * self.y)
        self.vx, self.vy = 0, 0
        self.durability = 20

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / FPS, self.vy / FPS)

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
        self.rect = self.image.get_rect().move(x * TITLE_WIDTH, y * TITLE_HEIGHT)
        self.pos = self.x, self.y = self.rect.x / TITLE_WIDTH, self.rect.y / TITLE_HEIGHT


class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite_img, pos, *groups):
        super().__init__(_all_sprites, *groups)
        self.pos = self.x, self.y = pos
        self._init_sprite(sprite_img)
        self.vx, self.vy = 0, 0

    def update(self, *events, kill=False):
        if kill:
            self.kill()
        self.rect = self.rect.move(self.vx / FPS, self.vy / FPS)

    def _init_sprite(self, sprite_img):
        self.orig_image = sprite_img
        self.image = self.orig_image
        self.rect = self.image.get_rect().move(TITLE_SIZE[0] * self.x,
                                               TITLE_SIZE[1] * self.y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if obj not in _interface_sprites:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = RESOLUTION[0] // 2 - target.rect.x - target.rect.w // 2
        self.dy = RESOLUTION[1] // 2 - target.rect.y - target.rect.h // 2
