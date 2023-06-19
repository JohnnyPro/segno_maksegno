from pygame.locals import *
import pygame
import sys
from colors import *


class PowerIndicator:
    def __init__(self, surface, x=695, y=350, width=20, height=20, speed=4,
                 power_bar_height=150) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.POWER_BAR_Y = y
        self.width = width
        self.height = height
        self.power_bar_height = power_bar_height
        self.points = [(self.x, self.y), (self.x - self.width, self.y +
                                          self.height / 2), (self.x - self.width, self.y - self.height / 2)]
        self.speed = speed
        self.isUp = True
        self.isInMotion = True

        self.default_speed = speed

    def _set_points(self, x, y):
        return [(x, y), (x - self.width, y +
                         self.height / 2), (x - self.width, y - self.height / 2)]

    def stopMotion(self):
        self.isInMotion = False

    def startMotion(self):
        self.isInMotion = True

    def draw_power_indicator(self):
        pygame.draw.polygon(self.surface, WHITE, self.points)
        self.move_power_indicator()

    def getPowerAccuracy(self):
        '''
            This is the function that is going to be called to get the current position of the power indicator. In terms of percentage 0-1
        '''
        self.stopMotion()
        # the top of the power bar height
        top = self.POWER_BAR_Y - self.power_bar_height

        # current y location of the indicator
        currentY = self.y

        # this is the center part of the power bar , which is the ideal part to aim for
        sweetSpot = top + (self.power_bar_height/2)

        # this tells us how far we are from the spot
        accuracy = (sweetSpot - currentY) / sweetSpot

        return 1 + accuracy

    def move_power_indicator(self):
        if self.isInMotion:
            if (self.y >= self.POWER_BAR_Y):
                self.isUp = True

            elif (self.y <= self.POWER_BAR_Y - self.power_bar_height):
                self.isUp = False

            if self.isUp:
                self.y -= self.speed
            else:
                self.y += self.speed

            self.points = self._set_points(self.x, self.y)

    def set_speed(self, target, reverse_trip=False):
        """
        set speed based on the next target. should be faster as we 
        approach sunday

        ignore this, unused
        """

        targets = ["Monday", "Tuesday", "Wednesday",
                   "Thursday", "Friday", "Saturday", "Sunday"]
        multiplier = 1
        if reverse_trip:
            targets = targets.reverse()
            multiplier = 2

        self.speed = 4 + multiplier*(0.5*targets.index(target))

    def increase_speed(self):
        """
        increase indicator speed by 0.5 on successful turn
        """
        self.speed += 0.5

    def reset_speed(self):
        """
        reset to default speed on failed turn
        """
        self.speed = self.default_speed
