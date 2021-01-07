import sys
import pygame
import engine
import data


class Game:
    def __init__(self):
        pygame.init()
        self.running = False
        self._init_screen()
        self._init_camera()
        self.clock = pygame.time.Clock()
        self.game_state = engine.GameState.MAIN_MENU
        self._init_main_menu()

    def _init_main_menu(self):
        self._screen.fill(pygame.Color('Blue'))
        self.start_button = engine.Button('button', (5, 5), engine._button_sprites)
        self.quit_button = engine.Button('button', (5, 7), engine._button_sprites)

    def _init_playing(self):
        self._init_player()
        self._init_game_map()

    def _init_pause_menu(self):
        self._screen.fill(pygame.Color('Green'))
        self.back_game_button = engine.Button('button', (5, 5), engine._button_sprites)
        self.back_menu_button = engine.Button('button', (5, 7), engine._button_sprites)

    def _init_screen(self):
        self._screen = pygame.display.set_mode(data.RESOLUTION)
        pygame.display.set_caption('XYgame')

    def _init_player(self):
        self._character = engine.Player((5, 5))

    def _init_game_map(self):
        pass

    def _init_camera(self):
        pass

    def _main_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked():
                    self.game_state = engine.GameState.PLAYING
                    self._init_playing()
                elif self.quit_button.is_clicked():
                    self._terminate()

    def _playing_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                    self._move_events(event)
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = engine.GameState.PAUSE
                    self._init_pause_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (pygame.BUTTON_WHEELDOWN, pygame.BUTTON_WHEELUP):
                    self._character.change_equipped_item(event)
                self._attack_events(event)
        self._character.update_pos()

    def _pause_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_game_button.is_clicked():
                    self.game_state = engine.GameState.PLAYING
                elif self.back_menu_button.is_clicked():
                    self._init_main_menu()

    def run(self):
        self.running = True
        while self.running:
            self._main_loop()
        self._terminate()

    def _main_loop(self):
        self._process_events()
        self._update_camera()
        self._render_screen()
        self.clock.tick(data.FPS)

    def _process_events(self):
        self._events = pygame.event.get()
        if self.game_state == engine.GameState.MAIN_MENU:
            self._main_menu_process_events(self._events)
        elif self.game_state == engine.GameState.PLAYING:
            self._playing_process_events(self._events)
        elif self.game_state == engine.GameState.PAUSE:
            self._pause_menu_process_events(self._events)

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

    def _render_main_menu(self):
        self._screen.fill(pygame.Color('Blue'))
        engine._button_sprites.draw(self._screen)

    def _render_playing(self):
        self._screen.fill(pygame.Color('Black'))
        # engine._all_sprites.draw(self._screen)
        engine._character_sprites.draw(self._screen)
        engine._equipped_item_sprites.draw(self._screen)
        engine._bullet_sprites.draw(self._screen)
        engine._all_sprites.update(self._events)

    def _render_pause_menu(self):
        self._screen.fill(pygame.Color('Green'))
        engine._button_sprites.draw(self._screen)

    def _render_screen(self):
        if self.game_state == engine.GameState.MAIN_MENU:
            self._render_main_menu()
        elif self.game_state == engine.GameState.PLAYING:
            self._render_playing()
        elif self.game_state == engine.GameState.PAUSE:
            self._render_pause_menu()
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
