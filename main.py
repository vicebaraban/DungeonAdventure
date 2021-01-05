import pygame
import engine


class Game:
    def __init__(self):
        self.running = False

    def main_loop(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.main_loop()


if __name__ == '__main__':
    game = Game()
    game.run()
