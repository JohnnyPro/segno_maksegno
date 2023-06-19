from pygame.locals import *
import pygame
import sys

global WHITE
global BLACK
global GREEN
global RED

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def Test():
    ...


def main():

    pygame.init()
    window_size = (800, 700)

    surface = pygame.display.set_mode((window_size[0], window_size[1]))
    caption = pygame.display.set_caption("Segno Maksegno")
    clock = pygame.time.Clock()
    # defining players with their position and other needed info
    # can be implemented as a class
    # can't be asked to do it now

    players = [
        Player(surface=surface, name='Player-1'),
        Player(surface=surface, name='Player-2', isTurn=False, color=GREEN)
    ]

    currentTurn = 0
    power_bar = PowerBar(surface)
    power_indicator = PowerIndicator(surface)
    play_grid = PlayGrid(surface)

    # for registering 1 button press per 60fps
    button_pressed = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            # print(f'Button PRESSEEEEEEEEEEEEEEEEEEEEED {button_pressed}')
            if button_pressed:
                continue
            if not button_pressed:
                accuracy = power_indicator.getPowerAccuracy()
                button_pressed = True

        else:
            button_pressed = False

        # Handle key presses
        surface.fill(BLACK)
        # draw players
        for player in players:
            player.draw_player()

        # draw player grid
        play_grid.draw_playgrid()

        # get the player who touched this and apply the changes to them
        if button_pressed:
            try:
                player = players[currentTurn]
            except Exception as e:
                currentTurn = 0
                player = players[currentTurn]
            goal = player.nextTarget
            goalPos = play_grid.tiles[goal][0] + (play_grid.height / 2)
            playerTopY = player.jump(power=accuracy, goal=goalPos)
            isStamped = play_grid.grid_stamped(
                posBox=(playerTopY, playerTopY + player.height))
            print(isStamped)
            if isStamped:
                player.isTurn = False
                player.return_to_side_line()
                index = players.index(player)
                try:
                    player = players[index + 1]
                    player.take_turn()
                    player.isTurn = True
                except Exception as e:
                    player = players[0]
                    player.take_turn()
                    player.isTurn = True
            else:
                player.selectNextTarget()
                print(player.nextTarget)

            power_indicator.isInMotion = True

        power_bar.draw_powerbar()
        power_indicator.draw_power_indicator()

        clock.tick(60)
        pygame.display.update()


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


if __name__ == '__main__':
    main()