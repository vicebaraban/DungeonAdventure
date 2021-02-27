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
        pygame.mouse.set_visible(False)
        self.game_state = engine.GameState.MAIN_MENU
        self._init_main_menu()

    def _init_main_menu(self):
        engine._all_sprites.update(kill=True)
        self.start_button = engine.Button('b_start_game', (7, 6), engine._menu_sprites)
        self.quit_button = engine.Button('b_exit', (7, 8), engine._menu_sprites)
        pygame.mixer.Channel(0).play(data.main_menu_music, -1)

    def _init_playing(self):
        self._game_map = engine.GameMap('map1.txt')
        self._character = engine.Player(self._game_map.start_pos, engine._character_sprites, engine._player_sprites)
        self.ui = engine.Interface((0, 500), 'playing_ui')
        pygame.mixer.Channel(0).play(data.playing_music, -1)

    def _init_pause_menu(self):
        self.back_game_button = engine.Button('b_continue', (7, 6), engine._pause_sprites)
        self.back_menu_button = engine.Button('b_back_to_menu', (7, 8), engine._pause_sprites)

    def _init_final_menu(self):
        self.back_menu_button = engine.Button('b_back_to_menu', (7, 6), engine._pause_sprites)

    def _init_screen(self):
        self._screen = pygame.display.set_mode(data.RESOLUTION)
        pygame.display.set_caption('Dungeon Adventure')

    def _init_camera(self):
        self.camera = engine.Camera()

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
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                    self._character.change_equipped_item(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
            #    if event.button in (pygame.BUTTON_WHEELDOWN, pygame.BUTTON_WHEELUP):
            #        self._character.change_equipped_item(event)
                self._attack_events(event)
        self._character.update_pos()
        for enemy in engine._enemy_sprites:
            enemy.update_pos()

    def _pause_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_game_button.is_clicked():
                    self.game_state = engine.GameState.PLAYING
                    self.back_game_button.kill()
                    self.back_menu_button.kill()
                elif self.back_menu_button.is_clicked():
                    self.game_state = engine.GameState.MAIN_MENU
                    self._init_main_menu()

    def _final_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and self.back_menu_button.is_clicked():
                    self.game_state = engine.GameState.MAIN_MENU
                    self._init_main_menu()

    def _process_events(self):
        self._events = pygame.event.get()
        if self.game_state == engine.GameState.MAIN_MENU:
            self._main_menu_process_events(self._events)
        elif self.game_state == engine.GameState.PLAYING:
            self._playing_process_events(self._events)
        elif self.game_state == engine.GameState.PAUSE:
            self._pause_menu_process_events(self._events)
        elif self.game_state == engine.GameState.WIN or self.game_state == engine.GameState.LOSE:
            self._final_menu_process_events(self._events)

    def _move_events(self, event):
        self._character.move(event)

    def _attack_events(self, event):
        if event.button == pygame.BUTTON_LEFT:
            self._character.attack()

    def _terminate(self):
        pygame.quit()
        sys.exit()

    def _update_camera(self):
        self.camera.update(self._character)
        for sprite in engine._all_sprites:
            self.camera.apply(sprite)

    def _render_main_menu(self):
        self._screen.blit(data.images['menu_background'], [0, 0])
        engine._menu_sprites.draw(self._screen)

    def _render_playing(self):
        self._screen.fill('black')
        self._update_camera()
        self._game_map.draw(self._screen)
        engine._bullet_sprites.draw(self._screen)
        engine._character_sprites.draw(self._screen)
        engine._equipped_item_sprites.draw(self._screen)
        engine._interface_sprites.draw(self._screen)
        engine._bar_sprites.draw(self._screen)
        engine._all_sprites.update(self._events)
        if self._character.get_state() == engine.GameState.WIN:
            self.game_state = engine.GameState.WIN
            self._init_final_menu()
        if self._character.get_state() == engine.GameState.LOSE:
            self.game_state = engine.GameState.LOSE
            self._init_final_menu()
        for enemy in engine._enemy_sprites:
            enemy.move()
        if not len(engine._close_door_sprites.sprites()):
            self._character.char_state = engine.GameState.WIN
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(0).play(data.victory_music)

    def _render_pause_menu(self):
        self._screen.blit(data.images['pause_background'], [0, 0])
        engine._pause_sprites.draw(self._screen)

    def _render_final_menu(self, is_win):
        if is_win:
            self._screen.blit(data.images['victory_background'], [0, 0])
        else:
            self._screen.blit(data.images['lose_background'], [0, 0])
        engine._pause_sprites.draw(self._screen)

    def _render_screen(self):
        if self.game_state == engine.GameState.MAIN_MENU:
            self._render_main_menu()
        elif self.game_state == engine.GameState.PLAYING:
            self._render_playing()
        elif self.game_state == engine.GameState.PAUSE:
            self._render_pause_menu()
        elif self.game_state == engine.GameState.WIN:
            self._render_final_menu(True)
        elif self.game_state == engine.GameState.LOSE:
            self._render_final_menu(False)
        if pygame.mouse.get_focused():
            self._screen.blit(data.images['cursor'], pygame.mouse.get_pos())
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self._main_loop()
        self._terminate()

    def _main_loop(self):
        self._process_events()
        self._render_screen()
        self.clock.tick(data.FPS)
