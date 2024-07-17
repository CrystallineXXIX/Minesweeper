import pygame as pg 

from .colors import Colors
from .game import Game 

pg.font.init()


class Cell:
    flag = pg.image.load('flag.png')
    mine = pg.image.load('mine.png')
    font = pg.font.Font(None, 32)

    width = 100
    
    cells = []

    @staticmethod
    def set_width(width):
        Cell.width = width 
        Cell.flag = pg.transform.scale(Cell.flag, (width * 0.64, width * 0.64))
        Cell.mine = pg.transform.scale(Cell.mine, (width * 0.64, width * 0.64))
        Cell.font = pg.font.Font('bungee.ttf', int(width * 0.64))




    def __init__(self, coords):
        self.coords = coords
        self.rect = pg.Rect(coords.x * Cell.width, coords.y * Cell.width, Cell.width, Cell.width)

        self.ismine = False
        self.iscovered = True
        self.isflagged = False

        self.neighbours = []
        self.minecount = 0

        self.text = None 
        self.text_rect = None

        self.flag_rect = self.rect.copy().inflate((self.width * 0.64) - self.width, (self.width * 0.64) - self.width)

        if self.coords.x % 2 == self.coords.y % 2:
            self.color = Colors.CELL_COLOR_A
            self.color_open = Colors.CELL_COLOR_A_OPEN

        else:
            self.color = Colors.CELL_COLOR_B
            self.color_open = Colors.CELL_COLOR_B_OPEN

        Cell.cells.append(self)

    def draw(self, screen):
        if self.iscovered:
            pg.draw.rect(screen, self.color, self.rect)
            if self.isflagged:
                screen.blit(Cell.flag, self.flag_rect)
        else:
            pg.draw.rect(screen, self.color_open, self.rect)
            if self.ismine:
                screen.blit(Cell.mine, self.flag_rect) 
            else:
                screen.blit(self.text, self.text_rect)

    def update(self):
        if not self.ismine:
            open = False
            for cell in self.neighbours:
                if not cell.iscovered and cell.minecount == 0:
                    open = True
                    break

            if open:
                self.iscovered = False

        if Game.gameover:
            if self.ismine:
                self.iscovered = False


    def setup(self, mines):

        self.neighbours = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                x = int(self.coords.x + dx)
                y = int(self.coords.y + dy)

                if x < 0 or x >= Game.n or y < 0 or y >= Game.n:
                    continue

                self.neighbours.append(Game.grid[x][y])

        if self.coords in mines:
            self.ismine = True
            self.minecount = -1

        else:
            for neighbour in self.neighbours:
                if neighbour.coords in mines:
                    self.minecount += 1

        self.text = self.font.render(str(self.minecount) if self.minecount > 0 else '', True, Colors.TEXT)
        self.text_rect = self.text.get_rect(center=self.rect.center)

        



