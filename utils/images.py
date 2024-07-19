import pygame as pg 
from pygame.math import Vector2
from .colors import cpcn

def create_flag(width):
    flag = pg.Surface((width, width), pg.SRCALPHA)

    pg.draw.rect(flag, cpcn.overlay2.hex, (width * 0.05, width * 0.1, width * 0.075, width))
    pg.draw.polygon(flag, cpcn.blue.hex, [
        (0, 0),
        (width, width * 0.325),
        (0, width * 0.65)
    ])
    return flag 

def create_mine(width):
    mine = pg.Surface((width, width), pg.SRCALPHA)

    center = Vector2(width // 2, width // 2)
    pg.draw.circle(mine, cpcn.overlay2.hex, center, width * 0.35)
    pg.draw.circle(mine, cpcn.red.hex, center, width * 0.2)
    for i in range(8):
        pg.draw.polygon(mine, cpcn.overlay1.hex, [
            center + Vector2(width * 0.1, -width * 0.2).rotate(45 * i),
            center + Vector2(-width * 0.1, -width * 0.2).rotate(45 * i),
            center + Vector2(0, -width * 0.5).rotate(45 * i),
        ])

    return mine
