import sys
import pygame
import engine
import data


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
        self._screen = pygame.display.set_mode(data.RESOLUTION)
        pygame.display.set_caption('XYgame')

    def _init_player(self):
        self._character = engine.Player((5, 5))

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
            self._update_camera()
            self._render_screen()
            self.clock.tick(data.FPS)

    def _process_events(self):
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                    self._move_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (pygame.BUTTON_WHEELDOWN, pygame.BUTTON_WHEELUP):
                    self._character.change_equipped_item(event)
                self._attack_events(event)
        self._character.update_pos()

    def _move_events(self, event):

        self._character.move(event)

    def _attack_events(self, event):
        if event.button == pygame.BUTTON_LEFT:
            self._character.attack()

    def _terminate(self):
        pygame.quit()
        sys.exit()

    def _update_camera(self):
        pass

    def _render_screen(self):
        self._screen.fill(pygame.Color('Black'))
        # engine._all_sprites.draw(self._screen)
        engine._character_sprites.draw(self._screen)
        engine._equipped_item_sprites.draw(self._screen)
        engine._bullet_sprites.draw(self._screen)
        engine._all_sprites.update(self._events)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
