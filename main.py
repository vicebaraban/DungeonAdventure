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

    def main_loop(self):
        while self.running:
            self.screen.fill(pygame.Color('black'))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.terminate()
            # отрисовка
            # обновление
            self.clock.tick(FPS)
            pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.main_loop()

    def terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
