import pygame, sys, math, random
from pygame.locals import *

MENU_STATE = 0
GAME_STATE = 1
RULES_STATE = 2
QUIT_STATE = 3

FPS = 60

GAME_NAME = "DIVINE HEAVEN"

FONT = "fonts/pixeboy.ttf"

CAR_W, CAR_L = 100, 125

SEC_EVENT = 2
END_COL_EVENT = 1

VICTIMS_IMAGES = []
for img in range(17):
    VICTIMS_IMAGES.append("images/victims/" + str(img) + ".jpg")


class Position:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str((self.x, self.y))

    def to_drawing(self):
        return self.x, self.y


class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def get_scale(self):
        return self.w/self.h

    def scale_up(self, scale):
        if self.w * scale > self.h:
            self.h = self.w * scale
        else:
            self.w = self.h * 1/scale

    def scale_down(self, scale):
        if self.w * scale < self.h:
            self.h = self.w * scale
        else:
            self.w = self.h * 1/scale

    def increase(self, width):
        scale = self.get_scale()
        self.w += width
        self.h = self.w // scale

    def __str__(self):
        return str((self.w, self.h))


SCREEN_SIZE = Size(500, 600)

TIME_POS = Position(75, 20)
DRAG_POS = Position(SCREEN_SIZE.w-100, 20)

TIME_CLR = (255, 255, 255)
DRAG_CLR = (255, 0, 250)


class Sprite:
    POS = Position(0, 0)
    SIZE = Size(0, 0)
    CLR = (0, 0, 0)

    def __init__(self, screen, pos=POS, size=SIZE, clr=CLR):
        self.pos = pos
        self.size = size
        self.clr = clr
        self.screen = screen

    def left_corner(self):
        return self.pos.x-self.size.w//2

    def right_corner(self):
        return self.pos.x+self.size.w//2

    def top_corner(self):
        return self.pos.y-self.size.h//2

    def bottom_corner(self):
        return self.pos.y+self.size.h//2

    def hits(self, other):
        return not (self.left_corner() > other.right_corner() or
                    other.left_corner() > self.right_corner() or
                    self.bottom_corner() < other.top_corner() or
                    other.bottom_corner() < self.top_corner())

    def will_hit(self, other):
        return not (self.left_corner() > other.right_corner() or
                    other.left_corner() > self.right_corner())

    def draw(self):
        pass

    def update(self, div_speed):
        pass
