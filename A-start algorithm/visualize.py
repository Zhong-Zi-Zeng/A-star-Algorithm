import pygame
import numpy as np


class GUI:
    def __init__(self, win_height=500, win_width=500):
        pygame.init()
        pygame.display.set_caption("Map")

        # window size
        self.win_height = win_height
        self.win_width = win_width
        self.win_screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.win_screen.fill((255, 255, 255))

        # square size
        self.square_size = 20

        # map size
        self.map_h = self.win_height // self.square_size
        self.map_w = self.win_width // self.square_size

    def set_map(self, row, col, color):
        x = row * self.square_size
        y = col * self.square_size

        pygame.draw.rect(self.win_screen, color, [x, y, self.square_size, self.square_size])

    def create_map(self, start, end, random_factor=0.03):
        map = np.zeros((self.map_h, self.map_w))

        for row in range(self.map_h):
            for col in range(self.map_w):
                if np.random.random() < random_factor:
                    map[row, col] = 1

        map[start[0], start[1]] = 0
        map[end[0], end[1]] = 0

        return map

    def show_map(self, map):
        for row in range(self.map_h):
            for col in range(self.map_w):
                if map[row, col] == 1:
                    self.set_map(row, col, (0, 0, 0))
