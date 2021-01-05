import sys
import pygame
import engine

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 600


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('XYgame')
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.running = False

    def _main_loop(self):
        while self.running:
            self._process_events()
            self.screen.fill('black')
            # отрисовка
            # обновление
            self.clock.tick(FPS)
            pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self._main_loop()

    def _terminate(self):
        pygame.quit()
        sys.exit()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()


if __name__ == '__main__':
    game = Game()
    game.run()
