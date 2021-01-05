import sys
import pygame
import engine

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 600


class Game:
    def __init__(self):
        pygame.init()
        self.running = False
        self.clock = pygame.time.Clock()
        self._init_screen()
        self._init_player()
        self._init_game_map()
        self._init_camera()

    def _init_screen(self):
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('XYgame')

    def _init_player(self):
        pass

    def _init_game_map(self):
        pass

    def _init_camera(self):
        pass

    def run(self):
        self.running = True
        self._main_loop()
        self._terminate()

    def _main_loop(self):
        while self.running:
            self._process_events()
            self.screen.fill('black')
            # отрисовка
            # обновление
            self.clock.tick(FPS)
            pygame.display.flip()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()

    def _terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
