from basic import *
from copy import deepcopy


class Opponent(Sprite):
    CLR = (10, 10, 10)
    IMG_PATH = "images/opponents/opponent.png"
    SIZE = Size(CAR_W, CAR_L)

    EVENT = 4
    T_RANGE = 1500, 2500

    def __init__(self, screen, pos, speed):
        super().__init__(screen, pos, self.SIZE, self.CLR)
        self.speed = speed

        self.img = pygame.image.load(self.IMG_PATH).convert()
        image_size = Size(self.img.get_width(), self.img.get_height())
        image_scale = image_size.get_scale()
        self.size.h = self.size.w // image_scale
        self.img = pygame.transform.scale(self.img, (self.size.w, self.size.h))
        self.img.set_colorkey((0, 0, 0))

    def draw(self):
        self.screen.blit(self.img, (self.pos.x-self.size.w/2, self.pos.y-self.size.h/2))

    def update(self, div_speed):
        self.pos.y -= self.speed - div_speed


class Bullet(Sprite):
    CLR = (255, 255, 255)
    IMG_PATH = "images/bullets/vib_bullet.jpg"
    SOUND_PATH = "sounds/bullet.mp3"
    SIZE = Size(5, 10)
    SPEED = 3

    def __init__(self, screen, pos):
        super().__init__(screen, pos, self.SIZE, self.CLR)

        self.sound = pygame.mixer.Sound(self.SOUND_PATH)
        pygame.mixer.Sound.play(self.sound)

        self.img = pygame.image.load(self.IMG_PATH).convert()
        image_size = Size(self.img.get_width(), self.img.get_height())
        image_scale = image_size.get_scale()
        self.size.h = self.size.w / image_scale
        self.img = pygame.transform.scale(self.img, (self.size.w, self.size.h))
        self.img.set_colorkey((255, 255, 255))

    def draw(self):
        self.screen.blit(self.img, (self.pos.x-self.size.w/2, self.pos.y-self.size.h/2))

    def update(self, div_speed):
        self.pos.y -= self.SPEED + div_speed


class Victim(Sprite):
    CLR = (255, 10, 10)
    SIZE = Size(125, 125)

    EVENT = 3
    T_RANGE = 5000, 10000

    def __init__(self, screen, pos, img_path):
        super().__init__(screen, pos, deepcopy(self.SIZE), self.CLR)
        self.img_path = img_path
        self.img_unscaled = pygame.image.load(img_path).convert()
        image_size = Size(self.img_unscaled.get_width(), self.img_unscaled.get_height())
        image_scale = image_size.get_scale()
        self.size.w = self.size.h * image_scale // 2
        self.img = pygame.transform.scale(self.img_unscaled, (self.size.w*2, self.size.h))

        self.alpha = 255
        self.img.set_alpha(self.alpha)

        self.area = 0, 0, self.size.w, self.size.h
        self.transforming = False

    def draw(self):
        self.screen.blit(self.img, (self.pos.x-self.size.w/2, self.pos.y-self.size.h/2), self.area)

    def transform(self):
        self.transforming = True

    def update(self, div_speed):
        self.pos.y += div_speed

        if self.transforming:
            self.alpha -= self.size.w//25
            if self.alpha <= 0:
                self.alpha = 0
            else:
                self.size.increase(5)
                self.area = self.size.w, 0, self.size.w * 2, self.size.h
            self.img = pygame.transform.scale(self.img_unscaled, (self.size.w * 2, self.size.h))
            self.img.set_alpha(self.alpha)
            self.img.convert_alpha()


