from pygame.locals import *
import pygame
import sys
from colors import *


class Player:
    def __init__(self, surface, name="Player - 1", width=50, height=50,
                 isTurn=True, nextTarget="Monday", lastLap=False, color=RED):
        self.current_position = [425, 590] if isTurn else [225, 490]
        self.isTurn = isTurn
        self.width = width
        self.height = height
        self.surface = surface
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()
        self.name = name
        self.nextTarget = nextTarget
        self.lastLap = lastLap
        self.color = color

    def return_to_side_line(self):
        self.current_position = [225, 490]
        self.isTurn = False

    def take_turn(self):
        self.current_position = [425, 590]
        self.isTurn = True

    def key_handler(self, keys):
        speed = 10
        if keys[K_o]:
            self.move_player(0, -speed)

        if keys[K_l]:
            self.move_player(0, speed)

        if keys[K_k]:
            self.move_player(-speed, 0)

        if keys[K_SEMICOLON]:
            self.move_player(speed, 0)

    def move_player(self, x, y):
        player_width = self.width
        player_height = self.height

        if self.current_position[0] + player_width + x <= self.surface_width and self.current_position[0] + (x) >= 0:
            self.current_position[0] += x

        elif self.current_position[0] + player_width + x > self.surface_width:
            self.current_position[0] = self.surface_width - player_width

        elif self.current_position[0] + x < 0:
            self.current_position[0] = 0

        if self.current_position[1] + player_height + y <= self.surface_height and self.current_position[1] + (y) >= 0:
            self.current_position[1] += y

        elif self.current_position[1] + player_height + y > self.surface_height:
            self.current_position[1] = self.surface_height - player_height

        elif self.current_position[1] + y < 0:
            self.current_position[1] = 0

        print(self.current_position)
        self.draw_player(self.current_position)

    def jump(self, power, goal):
        # print(f"Goal : {goal} - Current : {self.current_position[1]} ")
        changeNeeded = goal - self.current_position[1]
        # print(f"Change Needed : {changeNeeded}")
        finalPos = self.current_position[1] + changeNeeded * power
        # print(f"FinalPos : {finalPos}")
        if self.lastLap:
            self.current_position[1] = finalPos + \
                (self.height / 2) * (changeNeeded / changeNeeded)

        self.current_position[1] = finalPos - \
            (self.height / 2) * (changeNeeded / changeNeeded)
        return self.current_position[1]

    def draw_player(self, pos=None):
        if pos != None:
            player_rect = Rect(pos[0], pos[1], self.width, self.height)
        player_rect = Rect(
            self.current_position[0], self.current_position[1], self.width, self.height)
        pygame.draw.rect(self.surface, self.color, player_rect, 1)

    def selectNextTarget(self):
        nextTargets = {
            "Monday": "Tuesday",
            "Tuesday": "Wednesday",
            "Wednesday": "Thursday",
            "Thursday": "Friday",
            "Friday": "Saturday"
        }

        reverseNextTargets = {
            "Saturday": "Friday",
            "Friday": "Thursday",
            "Thursday": "Wednesday",
            "Wednesday": "Tuesday",
            "Tuesday": "Monday"
        }

        if not self.lastLap:
            try:
                self.nextTarget = nextTargets[self.nextTarget]
            except:
                self.lastLap = True
                self.nextTarget = reverseNextTargets[self.nextTarget]
        else:
            try:
                self.nextTarget = reverseNextTargets[self.nextTarget]
            except:
                self.lastLap = False
                self.nextTarget = nextTargets[self.nextTarget]
