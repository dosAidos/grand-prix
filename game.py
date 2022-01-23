from background import *
from divine import *
from ui import *


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_SIZE.w, SCREEN_SIZE.h))

        pygame.mixer.music.load('sounds/ymca.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)

        self.time_spent = 0
        self.time_font = pygame.font.Font(FONT, 50)
        self.time_txt = self.time_font.render(str(self.time_spent), True, TIME_CLR)

        self.drag_points = 0
        self.drag_font = pygame.font.Font(FONT, 50)
        self.drag_txt = self.time_font.render(str(self.time_spent), True, DRAG_CLR)

        self.bkg = Background(self.screen)
        self.divine = Divine(self.screen)
        self.bullets = []
        self.victims = []
        self.opponents = []

        pygame.time.set_timer(SEC_EVENT, 1000)
        pygame.time.set_timer(Victim.EVENT, random.randrange(Victim.T_RANGE[0], Victim.T_RANGE[1]), 1)
        pygame.time.set_timer(Opponent.EVENT, random.randrange(Opponent.T_RANGE[0], Opponent.T_RANGE[1]), 1)

    def loop(self):
        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return QUIT_STATE
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        start = True
                        self.divine.accelerating = True

            self.bkg.draw()
            self.divine.draw()
            self.screen.blit(self.time_txt, (TIME_POS.x, TIME_POS.y))
            self.screen.blit(self.drag_txt, (DRAG_POS.x, DRAG_POS.y))
            pygame.display.flip()
            pygame.display.update()

        i = 0
        #while i <= 1:
        while i <= len(VICTIMS_IMAGES):
            for event in pygame.event.get():
                if event.type == QUIT:
                    return QUIT_STATE
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.bullets.append(self.divine.fire())
                    if event.key == pygame.K_LEFT:
                        self.divine.moving_left = True
                    if event.key == K_RIGHT:
                        self.divine.moving_right = True
                    if event.key == K_UP:
                        self.divine.accelerating = True
                    if event.key == K_DOWN:
                        self.divine.braking = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.divine.moving_left = False
                    if event.key == K_RIGHT:
                        self.divine.moving_right = False
                    if event.key == K_UP:
                        self.divine.accelerating = False
                    if event.key == K_DOWN:
                        self.divine.braking = False
                elif event.type == SEC_EVENT:
                    self.time_spent += 1
                    self.time_txt = self.time_font.render(str(self.time_spent), True, TIME_CLR)
                elif event.type == Victim.EVENT:
                    if self.divine.speed != 0 and i < len(VICTIMS_IMAGES):
                        vic = Victim(self.screen, Position(
                            random.randrange(int(
                                SCREEN_SIZE.w - Frontier.SIZE.w * 2 - Victim.SIZE.w)) + Frontier.SIZE.w + Victim.SIZE.w // 2,
                            -Victim.SIZE.h // 2),
                                     VICTIMS_IMAGES[i])
                        self.victims.append(vic)
                    pygame.time.set_timer(Victim.EVENT, random.randrange(Victim.T_RANGE[0], Victim.T_RANGE[1]), 1)
                    i += 1
                elif event.type == Opponent.EVENT:
                    opp = Opponent(self.screen, Position(
                        random.randrange(int(SCREEN_SIZE.w - Frontier.SIZE.w * 2 - Opponent.SIZE.w))
                        + Frontier.SIZE.w + Opponent.SIZE.w // 2,
                        -Opponent.SIZE.h // 2),
                                   random.random() * 2 + 2)
                    ok_pos = True
                    for other in self.opponents:
                        if other.will_hit(opp):
                            ok_pos = False
                    if ok_pos:
                        self.opponents.append(opp)
                    pygame.time.set_timer(Opponent.EVENT, random.randrange(Opponent.T_RANGE[0], Opponent.T_RANGE[1]), 1)
                elif event.type == END_COL_EVENT:
                    self.divine.end_collision()
                    self.bkg.end_collision()

            for bullet in self.bullets:
                for vic in self.victims:
                    if bullet.hits(vic):
                        self.drag_points += 1
                        self.drag_txt = self.drag_font.render(str(self.drag_points), True, DRAG_CLR)
                        vic.transform()
                        self.bullets.remove(bullet)

            if self.divine.hits(self.bkg.frontiers[0]):
                self.divine.moving_left = False
            if self.divine.hits(self.bkg.frontiers[1]):
                self.divine.moving_right = False

            for opp in self.opponents:
                if opp.hits(self.divine):
                    self.divine.collision()
                    self.bkg.collision()
                    pygame.time.set_timer(END_COL_EVENT, 150, 1)

            objects = [self.bkg, self.divine] + self.opponents + self.victims + self.bullets
            for obj in objects:
                obj.update(self.divine.speed)
            for obj in objects:
                obj.draw()

            self.remove_from_screen(self.victims)
            self.remove_from_screen(self.opponents)
            self.remove_from_screen(self.bullets)

            self.screen.blit(self.time_txt, (TIME_POS.x, TIME_POS.y))
            self.screen.blit(self.drag_txt, (DRAG_POS.x, DRAG_POS.y))

            pygame.display.flip()
            pygame.display.update()

            self.clock.tick(FPS)

        menu_btn = Button(self.screen,
                           Position(SCREEN_SIZE.w/2, SCREEN_SIZE.h*1/3),
                           "MENU")

        quit_btn = Button(self.screen,
                          Position(SCREEN_SIZE.w/2, SCREEN_SIZE.h*2/3),
                          "QUIT")

        buttons = [menu_btn, quit_btn]

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return QUIT_STATE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_btn.clicked(pygame.mouse):
                        menu_btn.press_down()
                    if quit_btn.clicked(pygame.mouse):
                        quit_btn.press_down()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if menu_btn.clicked(pygame.mouse):
                        pygame.mixer.music.load('sounds/tgchi.mp3')
                        pygame.mixer.music.play(-1)
                        return MENU_STATE
                    if quit_btn.clicked(pygame.mouse):
                        return QUIT_STATE

            self.divine.finish(.7)
            for opp in self.opponents:
                opp.update(2)

            self.bkg.draw()
            for opp in self.opponents:
                opp.draw()
            if self.divine.bottom_corner() >= 0:
                self.divine.draw()
            for btn in buttons:
                btn.draw()
            self.screen.blit(self.time_txt, (TIME_POS.x, TIME_POS.y))
            self.screen.blit(self.drag_txt, (DRAG_POS.x, DRAG_POS.y))
            pygame.display.flip()
            pygame.display.update()

    @staticmethod
    def remove_from_screen(obj_list):
        for obj in obj_list:
            if obj.top_corner() > SCREEN_SIZE.h or obj.bottom_corner() < 0:
                obj_list.remove(obj)
