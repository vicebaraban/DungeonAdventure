import sys
import pygame
import engine
import constants


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
        self.screen = pygame.display.set_mode(constants.RESOLUTION)
        pygame.display.set_caption('XYgame')

    def _init_player(self):
        self._character = engine.Player((0, 0))

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
            self.clock.tick(constants.FPS)
            pygame.display.flip()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.KEYDOWN:
                self._move_events(event)

    def _move_events(self, event):
        if event.key == pygame.K_DOWN:
            self._character.move(engine.MoveDirection.DOWN)
        elif event.key == pygame.K_UP:
            self._character.move(engine.MoveDirection.UP)
        elif event.key == pygame.K_RIGHT:
            self._character.move(engine.MoveDirection.RIGHT)
        elif event.key == pygame.K_LEFT:
            self._character.move(engine.MoveDirection.LEFT)

    def _terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
