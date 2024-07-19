import pygame as pg 
import sys

from random import randint
from pygame.math import Vector2

import utils

# ----------------- Pygame Setup ----------------- #
pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Minesweeper")

bigfont = pg.font.Font('bungee.ttf', 64)
font = pg.font.Font('bungee.ttf', 32)

# ----------------- Vars ----------------- #
gameover_text = bigfont.render("DEFEAT", True, utils.Colors.LOST)
gameover_text_rect = gameover_text.get_rect(center=(360, 360))

won_text = bigfont.render("VICTORY", True, utils.Colors.WON)
won_text_rect = won_text.get_rect(center=(360, 360))

menu_text = bigfont.render("MINESWEEPER", True, utils.Colors.TEXT[1])
menu_text_rect = menu_text.get_rect(center=(360, 100))

menu_dialog_text = font.render("SPACE TO START", True, utils.Colors.TEXT[2])
menu_dialog_text_rect = menu_dialog_text.get_rect(center=(360, 600))

change_difficulty_text = font.render("CHANGE DIFFICULTY WITH ARROW KEYS", True, utils.Colors.TEXT[4])
change_difficulty_text_rect = change_difficulty_text.get_rect(center=(360, 400))

# ----------------- Functions ----------------- #
def handle_left_click(pos):
    for cell in utils.Cell.cells:
        if cell.rect.collidepoint(pos):
            if not cell.isflagged:
                cell.iscovered = False
                break

def handle_right_click(pos):
    for cell in utils.Cell.cells:
        if cell.rect.collidepoint(pos):
            if cell.iscovered:
                cell.isflagged = not cell.isflagged 
                break

def handle_middle_click(pos):
    for cell in utils.Cell.cells:
        if cell.rect.collidepoint(pos):
            if not cell.iscovered:
                count = 0
                for ncell in cell.neighbors:
                    if ncell.isflagged:
                        count += 1

                if count == cell.minecount:
                    for ncell in cell.neighbors:
                        if not ncell.isflagged:
                            ncell.iscovered = False

def setup(pos):
    mines = []
    while len(mines) < utils.Game.minecount:
        x = randint(0, utils.Game.n -1)
        y = randint(0, utils.Game.n -1)

        if (x, y) not in mines + [(pos[0] // utils.Cell.width, pos[1] // utils.Cell.width)]:
            mines.append((x, y))

    for cell in utils.Cell.cells:
        cell.setup(mines)

# ----------------- Screens ----------------- #
def menu():
    difficulties = ['easy', 'medium', 'hard']
    difficulty = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    difficulty -= 1 
                    difficulty %= 3
                    difficulty = abs(difficulty)

                if event.key == pg.K_RIGHT:
                    difficulty += 1 
                    difficulty %= 3 
                    difficulty = abs(difficulty)

                if event.key == pg.K_SPACE:
                    match difficulty:
                        case 0: 
                            utils.Game.set(8, 10)
                        case 1:
                            utils.Game.set(16, 40)
                        case 2: 
                            utils.Game.set(24, 90)
                    return main

        diff_text = bigfont.render(f"< {difficulties[difficulty]} >", True, utils.Colors.TEXT[5])
        diff_text_rect = diff_text.get_rect(center=(360, 300))


        screen.fill(utils.Colors.BACKGROUND)
        screen.blit(menu_text, menu_text_rect)
        screen.blit(diff_text, diff_text_rect)
        screen.blit(change_difficulty_text, change_difficulty_text_rect)
        screen.blit(menu_dialog_text, menu_dialog_text_rect)
        pg.display.flip()
        

def main():
    
    utils.Game.won = False
    utils.Game.gameover = False
    utils.Game.started = False
    utils.Cell.cells = []
    utils.Game.grid = []

    utils.Cell.set_width(720 // utils.Game.n)

    for x in range(utils.Game.n):
        row = []
        for y in range(utils.Game.n):
            row.append(utils.Cell(Vector2(x, y)))

        utils.Game.grid.append(row)


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
                elif event.button == 2 and not utils.Game.gameover and not utils.Game.won:
                    handle_middle_click(event.pos)
                elif event.button == 3 and not utils.Game.gameover and not utils.Game.won:
                    handle_right_click(event.pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and (utils.Game.gameover or utils.Game.won):
                    return menu

        if utils.Game.gameover:
            screen.fill(utils.Colors.BACKGROUND)
            for cell in utils.Cell.cells:
                cell.update()
                cell.draw(screen)
            pg.draw.rect(screen, utils.Colors.BANNER, (0, 300, 720, 120))
            screen.blit(gameover_text, gameover_text_rect)
            pg.display.flip()
        elif utils.Game.won:
            screen.fill(utils.Colors.BACKGROUND)
            for cell in utils.Cell.cells:
                cell.update()
                cell.draw(screen)
            pg.draw.rect(screen, utils.Colors.BANNER, (0, 300, 720, 120))
            screen.blit(won_text, won_text_rect)
            pg.display.flip()
        else:
            screen.fill(utils.Colors.BACKGROUND)

            for cell in utils.Cell.cells:
                cell.draw(screen, pg.mouse.get_pos())
                if cell.ismine and not cell.iscovered:
                    utils.Game.gameover = True

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

# ----------------- Main ----------------- #
if __name__ == "__main__":
    func = menu 
    while True:
        func = func()

