from pygame.locals import *
import pygame
import sys
from colors import *


class PowerBar:
    def __init__(self, surface, x=700, y=200, width=40, height=150):
        self.surface = surface
        self.height = height
        self.pz = y
        self.p0 = y + self.height
        self.x = x
        self.width = width

    def draw_powerbar(self):
        power_bar = Rect(self.x, self.pz, self.width, self.height)

        pygame.draw.rect(self.surface, (WHITE), power_bar, 1)
