import pygame
from display import Button

pygame.init()


class GameStates:
    def __init__(self, display):
        self.state = 0
        self.display = display

        # main_menu variables
        self.fixed_bg = pygame.image.load("assets/main_menu.png").convert()
        self.bg = pygame.transform.scale(self.fixed_bg, self.display.frame.size)
        self.button_img = pygame.image.load("assets/red_button.png").convert_alpha()
        self.buttons = []
        self.color = "white"
        self.btns_text = ["Play", "Levels", "Settings", "Quit"]

        # options vars
        self.test = pygame.image.load("assets/test2.jpg").convert_alpha()

        self.mask_img = pygame.image.load("assets/test1.png").convert_alpha()

    def states_manger(self, screen_scale):
        run = True
        s_w, s_h = screen_scale
        if self.state == 0:
            run = self.main_menu()
        elif self.state == 1:
            self.game()
        elif self.state == 2:
            self.levels()
        elif self.state == 3:
            self.options()

        return run

    def main_menu(self):
        # background
        self.bg = pygame.transform.scale(self.fixed_bg, self.display.frame.size)
        # sets buttons
        self.buttons = []
        font_size = int(0.04 * self.display.frame.height)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        h = 0.072
        gap = 0.045
        width, height = 0.22 * self.display.frame.width, h * self.display.frame.height
        x = self.display.frame.x + 0.68 * self.display.frame.width
        fr_y = self.display.frame.y
        rel_pos = []
        for i in range(4):
            rel_pos.append((x, fr_y + (0.36 + h / 2 + (h + gap) * i) * self.display.frame.height))
            btn = Button(self.display.screen, self.btns_text[i], self.color, font, rel_pos[i], self.button_img, width,
                         height)
            self.buttons.append(btn)

        # draw
        self.display.screen.blit(self.bg, self.display.frame)
        for btn in self.buttons:
            btn.draw()

        # if clicked
        if self.buttons[0].clicked():
            self.state = 1
            return True
        if self.buttons[1].clicked():
            self.state = 2
            return True
        if self.buttons[2].clicked():
            self.state = 3
            return True
        if self.buttons[3].clicked():
            return False
        return True

    def game(self):
        pygame.draw.rect(self.display.screen, "yellow", (300, 500, 400, 200), border_radius=20)

    def levels(self):
        pass

    def options(self):
        # board
        board_rect = pygame.Rect(self.display.frame.x + 0.3 * self.display.frame.width / 2,
                                 self.display.frame.y + 0.3 * self.display.frame.height / 2, 0.7 * self.display.frame.width, 0.7 * self.display.frame.height)
        surface = pygame.Surface(board_rect.size, masks=None)
        self.scaled_bg = pygame.transform.scale(self.test, (0.7 * self.display.frame.width, 0.7 * self.display.frame.height))
        self.scaled_img = pygame.transform.scale(self.mask_img, (0.7 * self.display.frame.width, 0.7 * self.display.frame.height))
        self.scaled_bg.blit(self.scaled_img, (0, 0))
        self.scaled_bg.set_colorkey("black")

        self.display.screen.blit(self.scaled_bg, board_rect.topleft)
