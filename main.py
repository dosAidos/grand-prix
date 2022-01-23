from menu import *
from game import *


if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption(GAME_NAME)

    pygame.mixer.init()
    pygame.mixer.music.load('sounds/tgchi.mp3')
    pygame.mixer.music.play(-1)

    state = MENU_STATE
    while True:
        if state == MENU_STATE:
            menu = Menu()
            state = menu.loop()

        if state == GAME_STATE:
            game = Game()
            state = game.loop()

        if state == RULES_STATE:
            rules = Rules()
            state = rules.loop()

        if state == QUIT_STATE:
            pygame.quit()
            sys.exit()


