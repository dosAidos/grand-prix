from sprites import *


class Divine(Sprite):
    CLR = (255, 0, 200)
    IMG_PATH = "images/divine/divine.png"
    FLAMES_PATH = "images/divine/flames.png"
    CRASH_SOUND = "sounds/short_crash.mp3"
    POS = Position(SCREEN_SIZE.w / 2, SCREEN_SIZE.h)
    SIZE = Size(CAR_W, CAR_L)
    FLAMES_SIZE = Size(100, 100)
    MAX_SPEED = 10

    def __init__(self, screen):
        super().__init__(screen, self.POS, self.SIZE, self.CLR)
        self.speed = 0
        self.accelerating = False
        self.braking = False
        self.moving_left = False
        self.moving_right = False

        self.crash_sound = pygame.mixer.Sound(self.CRASH_SOUND)

        self.img = pygame.image.load(self.IMG_PATH).convert()
        image_size = Size(self.img.get_width(), self.img.get_height())
        image_scale = image_size.get_scale()
        self.size.h = self.size.w // image_scale
        self.pos.y = SCREEN_SIZE.h-self.size.h/2
        self.img = pygame.transform.scale(self.img, (self.size.w, self.size.h))
        self.img.set_colorkey((0, 0, 0))

        self.end = False
        self.flames = pygame.image.load(self.FLAMES_PATH).convert()
        self.flames = pygame.transform.scale(self.flames, (self.FLAMES_SIZE.w, self.FLAMES_SIZE.h))
        self.flames.set_colorkey((0, 0, 0))


    def draw(self):
        self.screen.blit(self.img, (self.pos.x-self.size.w/2, self.pos.y-self.size.h/2))
        self.screen.blit(self.flames, (self.pos.x - self.size.w / 2 + 12, self.pos.y + self.size.h / 2 + 7))

    def update(self, _):
        if not(self.moving_left and self.moving_right):
            if self.moving_left:
                self.move_left(5)
            if self.moving_right:
                self.move_right(5)

        if not(self.accelerating and self.braking):
            if self.accelerating and self:
                self.speed_up(.015)
            elif self.braking and self:
                self.slow_down(.1)
            else:
                self.slow_down(.02)

    def move_left(self, val):
        self.pos.x -= val

    def move_right(self, val):
        self.pos.x += val

    def finish(self, speed):
        self.end = True
        self.pos.y -= speed

    def collision(self):
        pygame.mixer.Sound.play(self.crash_sound)
        self.slow_down(5)
        self.moving_left = not self.moving_left
        self.moving_right = not self.moving_right

    def end_collision(self):
        self.moving_left = False
        self.moving_right = False

    def slow_down(self, val):
        self.speed -= val
        if self.speed < 0:
            self.speed = 0

    def speed_up(self, val):
        self.speed += val
        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED

    def fire(self):
        return Bullet(self.screen, Position(self.pos.x, self.pos.y - self.size.h / 2))
