import pygame as pg  

class Game:
    gameover = False
    started = False
    won = False
    grid = []

    n = 0
    minecount = 0

    @staticmethod
    def set(n, minecount):
        Game.n = n
        Game.minecount = minecount
