import pygame as pg 
import sys

from random import randint
from pygame.math import Vector2

import utils

pg.init()
screen = pg.display.set_mode((720, 720))

utils.Game.set(10, 5)
utils.Cell.set_width(720 // utils.Game.n)


def handle_left_click(pos):
    for cell in utils.Cell.cells:
        if cell.rect.collidepoint(pos):
            if not cell.isflagged:
                cell.iscovered = False
                if cell.ismine:
                    utils.Game.gameover = True
                    break
                break

def handle_right_click(pos):
    for cell in utils.Cell.cells:
        if cell.rect.collidepoint(pos):
            if cell.iscovered:
                cell.isflagged = not cell.isflagged 
                break

def setup(pos):
    mines = []
    while len(mines) < utils.Game.minecount:
        x = randint(0, utils.Game.n -1)
        y = randint(0, utils.Game.n -1)

        if (x, y) not in mines + [(pos[0] // utils.Cell.width, pos[1] // utils.Cell.width)]:
            mines.append((x, y))

    for cell in utils.Cell.cells:
        cell.setup(mines)


for x in range(utils.Game.n):
    row = []
    for y in range(utils.Game.n):
        row.append(utils.Cell(Vector2(x, y)))

    utils.Game.grid.append(row)

def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:

                if not utils.Game.started:
                    utils.Game.started = True
                    setup(event.pos)

                if event.button == 1 and not utils.Game.gameover and not utils.Game.won:
                    handle_left_click(event.pos)
                elif event.button == 3 and not utils.Game.gameover and not utils.Game.won:
                    handle_right_click(event.pos)
        if utils.Game.gameover:
            screen.fill(utils.Colors.BACKGROUND)
            for cell in utils.Cell.cells:
                cell.update()
                cell.draw(screen)
            pg.draw.rect(screen, utils.Colors.RED, (0, 300, 720, 100))
            screen.blit(utils.Cell.font.render("Game Over", True, utils.Colors.TEXT), (200, 300))
            pg.display.flip()
        elif utils.Game.won:
            screen.fill(utils.Colors.BACKGROUND)
            pg.display.flip()
        else:
            screen.fill(utils.Colors.BACKGROUND)

            for cell in utils.Cell.cells:
                cell.draw(screen)

            if utils.Game.started:
                for cell in utils.Cell.cells:
                    cell.update()

                for cell in utils.Cell.cells:
                    if cell.ismine:
                        continue
                    if cell.iscovered:
                        break

                else:
                    utils.Game.won = True

            pg.display.flip()


main()

