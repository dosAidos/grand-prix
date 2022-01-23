from basic import *


class Background:
    TRACK_CLR = (100, 100, 100)
    CRASH_CLR = (255, 100, 100)

    def __init__(self, screen):
        self.screen = screen
        self.clr = self.TRACK_CLR
        self.frontiers = []
        self.frontiers.append(Frontier(self.screen, Position(Frontier.SIZE.w/2, SCREEN_SIZE.h/2)))
        self.frontiers.append(Frontier(self.screen, Position(SCREEN_SIZE.w-Frontier.SIZE.w/2, SCREEN_SIZE.h / 2)))

    def draw(self):
        self.screen.fill(self.clr)

        for ftr in self.frontiers:
            ftr.draw()

    def update(self, div_speed):
        for ftr in self.frontiers:
            ftr.update(div_speed)

    def collision(self):
        self.clr = self.CRASH_CLR

    def end_collision(self):
        self.clr = self.TRACK_CLR


class Frontier(Sprite):
    CLR = (180, 180, 75)
    BORDER_CLR = (0, 0, 0)

    MARK_NO = 7

    SIZE = Size(50, SCREEN_SIZE.h)

    def __init__(self, screen, pos):
        super().__init__(screen, pos, self.SIZE, self.CLR)

        self.marks = []
        for i in range(self.MARK_NO):
            y = self.size.h//self.MARK_NO*i
            self.marks.append(Mark(self.screen, Position(self.pos.x, y)))

    def draw(self):
        pygame.draw.rect(self.screen, self.CLR,
                         (self.left_corner(), self.top_corner(), self.SIZE.w, self.SIZE.h))
        pygame.draw.rect(self.screen, self.BORDER_CLR,
                         (self.left_corner(), self.top_corner()-3, self.SIZE.w, self.SIZE.h+6),
                         3)

        for mark in self.marks:
            mark.draw()

    def update(self, div_speed):
        for mark in self.marks:
            mark.update(div_speed)


class Mark(Sprite):
    CLR = (50, 150, 25)
    SIZE = Size(18, 18)

    def __init__(self, screen, pos):
        super().__init__(screen, pos, self.SIZE, self.CLR)

    def draw(self):
        pygame.draw.circle(self.screen, self.CLR, (self.pos.x, self.pos.y), self.size.w)

    def update(self, div_speed):
        self.pos.y += div_speed
        self.pos.y %= SCREEN_SIZE.h
