from basic import *
from ui import *
from menu import *


class Menu:
    SCREEN_SIZE = Size(1000, 600)
    BKG_IMG = "images/background/divine_nintendo.png"

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE.w, self.SCREEN_SIZE.h))

        pygame.mixer.music.set_volume(0.7)

        self.bkg = pygame.image.load(self.BKG_IMG).convert()
        image_size = Size(self.bkg.get_width(), self.bkg.get_height())
        image_scale = image_size.get_scale()
        self.bkg = pygame.transform.scale(self.bkg, (self.SCREEN_SIZE.h*image_scale, self.SCREEN_SIZE.h))

        self.start_btn = Button(self.screen,
                            Position(self.SCREEN_SIZE.w * 2/3, self.SCREEN_SIZE.h * 1/4),
                            "START")
        self.rules_btn = Button(self.screen,
                            Position(self.SCREEN_SIZE.w * 2 / 3, self.SCREEN_SIZE.h * 2/4),
                            "RULES")
        self.quit_btn = Button(self.screen,
                            Position(self.SCREEN_SIZE.w * 2/3, self.SCREEN_SIZE.h * 3/4),
                            "QUIT")
        self.buttons = [self.start_btn, self.rules_btn, self.quit_btn]

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return QUIT_STATE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.clicked(pygame.mouse):
                        self.start_btn.press_down()
                    if self.rules_btn.clicked(pygame.mouse):
                        self.rules_btn.press_down()
                    if self.quit_btn.clicked(pygame.mouse):
                        self.quit_btn.press_down()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.start_btn.clicked(pygame.mouse):
                        return GAME_STATE
                    if self.rules_btn.clicked(pygame.mouse):
                        return RULES_STATE
                    if self.quit_btn.clicked(pygame.mouse):
                        return QUIT_STATE
            self.screen.blit(self.bkg, (0, 0))
            for btn in self.buttons:
                btn.draw()
            pygame.display.update()


class Rules:
    SCREEN_SIZE = Menu.SCREEN_SIZE
    BKG_IMG = Menu.BKG_IMG

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE.w, self.SCREEN_SIZE.h))

        pygame.mixer.music.set_volume(0.7)

        self.bkg = pygame.image.load(self.BKG_IMG).convert()
        image_size = Size(self.bkg.get_width(), self.bkg.get_height())
        image_scale = image_size.get_scale()
        self.bkg = pygame.transform.scale(self.bkg, (self.SCREEN_SIZE.h*image_scale, self.SCREEN_SIZE.h))

        self.txt_box = Text_Box(self.screen,
                                Position(Menu.SCREEN_SIZE.w/2, Menu.SCREEN_SIZE.h/2-50),
                                """To play you can use the following commands:
                                \n-   UP ARROW to accelerate;
                                \n-   DOWN ARROW to brake;
                                \n-   LEFT ARROW to move left;
                                \n-   RIGHT ARROW to move right;
                                \n-   SPACE BAR to shoot bullets;
                                \n"Shoot" the maximum of victims to transform them, in the least amount of time
                                """)

        self.menu_btn = Button(self.screen,
                            Position(self.SCREEN_SIZE.w * 1/4, self.SCREEN_SIZE.h * 7/8),
                            "BACK")
        self.buttons = [self.menu_btn, ]

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return QUIT_STATE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_btn.clicked(pygame.mouse):
                        self.menu_btn.press_down()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.menu_btn.clicked(pygame.mouse):
                        return MENU_STATE
            self.screen.blit(self.bkg, (0, 0))
            self.txt_box.draw()
            for btn in self.buttons:
                btn.draw()
            pygame.display.update()
