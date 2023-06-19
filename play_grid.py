from pygame.locals import *
import pygame
import sys
from colors import *


class PlayGrid:
    def __init__(self, surface):
        self.surface = surface
        self.width = 200
        self.height = 70
        self.start = [350, 500]
        self.tiles = {"Monday": [0, 0, 0],
                      # [top y, bottom y, is_two_legged]
                      "Tuesday": [0, 0, 0],
                      "Wednesday": [0, 0, 0],
                      "Thursday": [0, 0, 1],
                      "Friday": [0, 0, 0],
                      "Saturday": [0, 0, 1],
                      }

    def draw_one_legged(self, y, x=350, width=200, height=70):
        one_legged_tile = Rect(x, y, width, height)
        pygame.draw.rect(self.surface, WHITE, one_legged_tile, 1)

    def draw_two_legged(self, y, x=350, width=200, height=70):
        first_part = Rect(x, y, width / 2, height)
        second_part = Rect(x + width / 2, y, width / 2, height)

        pygame.draw.rect(self.surface, WHITE, first_part, 1)
        pygame.draw.rect(self.surface, WHITE, second_part, 1)

    def draw_playgrid(self):
        current = self.start
        for tile in self.tiles:
            if self.tiles[tile][2] == 1:
                self.draw_two_legged(
                    y=current[1], x=current[0], width=self.width, height=self.height)
                self.tiles[tile] = [current[1], current[1] + self.height, 1]
                current[1] -= self.height

            else:
                self.draw_one_legged(
                    y=current[1], x=current[0], width=self.width, height=self.height)
                self.tiles[tile] = [current[1], current[1] + self.height, 0]
                current[1] -= self.height

        self.start = [350, 500]

    def grid_stamped(self, posBox):
        for tile in self.tiles:
            tilePos = self.tiles[tile]
            if posBox[0] <= tilePos[0] and posBox[1] >= tilePos[1]:
                return False
        return False
