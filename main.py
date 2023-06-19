from pygame.locals import *
from player import Player
from power_indicator import PowerIndicator
from power_bar import PowerBar
from play_grid import PlayGrid
import pygame
import sys
from colors import *


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
        Player(surface=surface, name='Player-1', isTurn=True, color=RED),
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
            pygame.time.wait(400)
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
            print(f'isStamped {isStamped}')
            if isStamped:
                player.isTurn = False
                player.return_to_side_line()
                index = players.index(player)
                try:
                    player = players[(index + 1) % 2]
                    player.take_turn()
                    player.isTurn = True
                    currentTurn = (currentTurn + 1) % 2
                except Exception as e:
                    print(e)
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


if __name__ == '__main__':
    main()
