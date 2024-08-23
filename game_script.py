import sys
import pygame
import engine_main
import game_data, game_objects


class Game:
    def __init__(self):
        pygame.init()
        print('''Welcome to Dungeon Adventure game. Good luck and have fun!''')
        self.running = False
        self._init_screen()
        self._init_camera()
        self._level = game_objects.LvlManager(game_data.maps)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        self.game_state = game_objects.GameState.MAIN_MENU
        self._init_main_menu(first_init=True)

    def _init_main_menu(self, first_init=False):
        engine_main._all_sprites.update(kill=True)
        self.start_button = engine_main.Button(game_data.images['b_start_game'], (7, 5), game_objects._menu_sprites)
        self.level_button = engine_main.Button(game_data.images['b_level_menu'], (7, 7), game_objects._menu_sprites)
        self.quit_button = engine_main.Button(game_data.images['b_exit'], (7, 9), game_objects._menu_sprites)
        if first_init:
            pygame.mixer.Channel(0).play(game_data.main_menu_music, -1)
            self.menu_music = None
        if pygame.mixer.Channel(0).get_sound() != self.menu_music:
            pygame.mixer.Channel(0).play(game_data.main_menu_music, -1)
        self.menu_music = pygame.mixer.Channel(0).get_sound()

    def _init_playing(self):
        self._game_map = game_objects.GameMap(self._level.maps[self._level.active_level])
        self._character = game_objects.Player(self._game_map.start_pos,
                                              game_objects._character_sprites, game_objects._player_sprites)
        self.ui = engine_main.Interface((0, 500), game_data.images['playing_ui'])
        pygame.mixer.Channel(0).play(game_data.playing_music, -1)

    def _init_pause_menu(self):
        self.back_game_button = engine_main.Button(game_data.images['b_continue'],
                                                   (7, 6), game_objects._pause_sprites)
        self.back_menu_button = engine_main.Button(game_data.images['b_back_to_menu'],
                                                   (7, 8), game_objects._pause_sprites)

    def _init_lose_menu(self):
        self.retry_button = engine_main.Button(game_data.images['b_retry_level'],
                                               (7, 6), game_objects._pause_sprites)
        self.back_menu_button = engine_main.Button(game_data.images['b_back_to_menu'],
                                                   (7, 8), game_objects._pause_sprites)

    def _init_win_menu(self, is_lust):
        if not is_lust:
            self.next_button = engine_main.Button(game_data.images['b_next_level'],
                                                  (7, 6), game_objects._pause_sprites)
        self.back_menu_button = engine_main.Button(game_data.images['b_back_to_menu'],
                                                   (7, 8), game_objects._pause_sprites)

    def _init_level_menu(self):
        b_list = ['b_level_1', 'b_level_2', 'b_level_3',
                  'b_level_4', 'b_level_5', 'b_level_6',
                  'b_level_7', 'b_level_8', 'b_level_9']
        engine_main._all_sprites.update(kill=True)
        self.lvl_1_button = engine_main.Button(game_data.images[b_list[0]], (3, 5), game_objects._level_sprites)
        self.lvl_2_button = engine_main.Button(game_data.images[b_list[1]], (5, 5), game_objects._level_sprites)
        self.lvl_3_button = engine_main.Button(game_data.images[b_list[2]], (7, 5), game_objects._level_sprites)
        # self.lvl_4_button = engine_main.Button(game_data.images[b_list[3]], (3, 6), game_objects._level_sprites)
        # self.lvl_5_button = engine_main.Button(game_data.images[b_list[4]], (5, 6), game_objects._level_sprites)
        # self.lvl_6_button = engine_main.Button(game_data.images[b_list[5]], (7, 6), game_objects._level_sprites)
        # self.lvl_7_button = engine_main.Button(game_data.images[b_list[6]], (3, 7), game_objects._level_sprites)
        # self.lvl_8_button = engine_main.Button(game_data.images[b_list[7]], (5, 7), game_objects._level_sprites)
        # self.lvl_9_button = engine_main.Button(game_data.images[b_list[8]], (7, 7), game_objects._level_sprites)
        self.current_lvl = engine_main.Button(game_data.images['lvl_active'], (11, 5), game_objects._level_sprites)
        self.current_lvl = engine_main.Button(game_data.images['lvl_max'], (13, 5), game_objects._level_sprites)
        self.current_lvl_button = engine_main.Button(game_data.images[b_list[self._level.active_level]], (11, 6),
                                                     game_objects._level_sprites)
        self.current_lvl_button = engine_main.Button(game_data.images[b_list[self._level.max_level]], (13, 6),
                                                     game_objects._level_sprites)
        self.back_menu_button = engine_main.Button(game_data.images['b_back_to_menu'], (7, 9),
                                                   game_objects._level_sprites)

    def _init_screen(self):
        self._screen = pygame.display.set_mode(game_data.RESOLUTION)
        pygame.display.set_caption('Dungeon Adventure')

    def _init_camera(self):
        self.camera = engine_main.Camera()

    def _main_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked():
                    self.game_state = game_objects.GameState.PLAYING
                    self._init_playing()
                elif self.level_button.is_clicked():
                    self.game_state = game_objects.GameState.LVL_MENU
                    self._init_level_menu()
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
                    self.game_state = game_objects.GameState.PAUSE
                    self._init_pause_menu()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0):
                    self._character.change_equipped(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (pygame.BUTTON_WHEELDOWN, pygame.BUTTON_WHEELUP):
                    self._character.change_equipped(event)
                self._attack_events(event)
        self._character.update_pos()
        for enemy in game_objects._enemy_sprites:
            enemy.update_pos()

    def _pause_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_game_button.is_clicked():
                    self.game_state = game_objects.GameState.PLAYING
                    self.back_game_button.kill()
                    self.back_menu_button.kill()
                elif self.back_menu_button.is_clicked():
                    self.game_state = game_objects.GameState.MAIN_MENU
                    self._init_main_menu()

    def _lose_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_menu_button.is_clicked():
                    self.game_state = game_objects.GameState.MAIN_MENU
                    self._init_main_menu()
                elif self.retry_button.is_clicked():
                    self.game_state = game_objects.GameState.PLAYING
                    engine_main._all_sprites.update(kill=True)
                    self._init_playing()

    def _win_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_menu_button.is_clicked():
                    self.game_state = game_objects.GameState.MAIN_MENU
                    self._init_main_menu()
                elif len(game_objects._pause_sprites) > 1 and self.next_button.is_clicked():
                    self._level.set_active_level(self._level.active_level + 2)
                    self.game_state = game_objects.GameState.PLAYING
                    engine_main._all_sprites.update(kill=True)
                    self._init_playing()

    def _level_menu_process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_menu_button.is_clicked():
                    self.game_state = game_objects.GameState.MAIN_MENU
                    self._init_main_menu()
                elif self.lvl_1_button.is_clicked() and self._level.is_free(1):
                    self._level.set_active_level(1)
                    self._init_level_menu()
                elif self.lvl_2_button.is_clicked() and self._level.is_free(2):
                    self._level.set_active_level(2)
                    self._init_level_menu()
                elif self.lvl_3_button.is_clicked() and self._level.is_free(3):
                    self._level.set_active_level(3)
                    self._init_level_menu()
                # elif self.lvl_4_button.is_clicked() and self._level.is_free(4):
                #     self._level.set_active_level(4)
                #     self._init_level_menu()
                # elif self.lvl_5_button.is_clicked() and self._level.is_free(5):
                #     self._level.set_active_level(5)
                #     self._init_level_menu()
                # elif self.lvl_6_button.is_clicked() and self._level.is_free(6):
                #     self._level.set_active_level(6)
                #     self._init_level_menu()
                # elif self.lvl_7_button.is_clicked() and self._level.is_free(7):
                #     self._level.set_active_level(7)
                #     self._init_level_menu()
                # elif self.lvl_8_button.is_clicked() and self._level.is_free(8):
                #     self._level.set_active_level(8)
                #     self._init_level_menu()
                # elif self.lvl_9_button.is_clicked() and self._level.is_free(9):
                #     self._level.set_active_level(9)
                #     self._init_level_menu()sss

    def _process_events(self):
        self._events = pygame.event.get()
        if self.game_state == game_objects.GameState.MAIN_MENU:
            self._main_menu_process_events(self._events)
        elif self.game_state == game_objects.GameState.PLAYING:
            self._playing_process_events(self._events)
        elif self.game_state == game_objects.GameState.PAUSE:
            self._pause_menu_process_events(self._events)
        elif self.game_state == game_objects.GameState.WIN:
            self._win_menu_process_events(self._events)
        elif self.game_state == game_objects.GameState.LOSE:
            self._lose_menu_process_events(self._events)
        elif self.game_state == game_objects.GameState.LVL_MENU:
            self._level_menu_process_events(self._events)

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
        for sprite in engine_main._all_sprites:
            self.camera.apply(sprite)

    def _render_main_menu(self):
        self._screen.blit(game_data.images['menu_background'], [0, 0])
        game_objects._menu_sprites.draw(self._screen)

    def _render_playing(self):
        self._screen.fill('black')
        self._update_camera()
        self._game_map.draw(self._screen)
        game_objects._bullet_sprites.draw(self._screen)
        game_objects._character_sprites.draw(self._screen)
        game_objects._char_effect_sprites.draw(self._screen)
        game_objects._equipped_item_sprites.draw(self._screen)
        engine_main._interface_sprites.draw(self._screen)
        game_objects._bar_sprites.draw(self._screen)
        game_objects._icon_tool_interface_sprites.draw(self._screen)
        engine_main._all_sprites.update(self._events)
        if self._character.get_state() == game_objects.GameState.WIN:
            self.game_state = game_objects.GameState.WIN
            self._init_win_menu(not self._level.unlock_next())
        if self._character.get_state() == game_objects.GameState.LOSE:
            self.game_state = game_objects.GameState.LOSE
            self._init_lose_menu()
        for enemy in game_objects._enemy_sprites:
            enemy.move()
        if not len(game_objects._close_door_sprites.sprites()):
            self._character.char_state = game_objects.GameState.WIN
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(0).play(game_data.victory_music)

    def _render_pause_menu(self):
        self._screen.blit(game_data.images['pause_background'], [0, 0])
        game_objects._pause_sprites.draw(self._screen)

    def _render_lose_menu(self):
        self._screen.blit(game_data.images['lose_background'], [0, 0])
        game_objects._pause_sprites.draw(self._screen)

    def _render_win_menu(self):
        self._screen.blit(game_data.images['victory_background'], [0, 0])
        game_objects._pause_sprites.draw(self._screen)

    def _render_level_menu(self):
        self._screen.blit(game_data.images['level_menu_background'], [0, 0])
        game_objects._level_sprites.draw(self._screen)

    def _render_screen(self):
        if self.game_state == game_objects.GameState.MAIN_MENU:
            self._render_main_menu()
        elif self.game_state == game_objects.GameState.PLAYING:
            self._render_playing()
        elif self.game_state == game_objects.GameState.PAUSE:
            self._render_pause_menu()
        elif self.game_state == game_objects.GameState.WIN:
            self._render_win_menu()
        elif self.game_state == game_objects.GameState.LOSE:
            self._render_lose_menu()
        elif self.game_state == game_objects.GameState.LVL_MENU:
            self._render_level_menu()
        if pygame.mouse.get_focused():
            self._screen.blit(game_data.images['cursor'], pygame.mouse.get_pos())
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self._main_loop()
        self._terminate()

    def _main_loop(self):
        self._process_events()
        self._render_screen()
        self.clock.tick(game_data.FPS)
