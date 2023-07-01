import pygame
from display import Button
from display import OnOff


pygame.init()


class GameStates:
    def __init__(self, display):
        self.state = 0
        self.display = display
        self.fx = self.display.frame.x
        self.fy = self.display.frame.y
        self.fw = self.display.frame.width
        self.fh = self.display.frame.height

        # button
        self.button_img = pygame.image.load("assets/red_button.png").convert_alpha()

        # main_menu variables
        self.fixed_bg = pygame.image.load("assets/main_menu.jpg").convert()
        self.bg = pygame.transform.scale(self.fixed_bg, self.display.frame.size)
        self.buttons = []
        self.color = "white"
        self.btns_text = ["Play", "Levels", "Options", "Quit"]

        # options vars
        # self.test = pygame.image.load("assets/test2.jpg").convert_alpha()
        # self.mask_img = pygame.image.load("assets/test1.png").convert_alpha()
        self.ON_img = pygame.image.load("assets/ON.png").convert_alpha()
        self.OFF_img = pygame.image.load("assets/OFF.png").convert_alpha()
        self.developer = False

    def states_manger(self, events, developer):
        run = True
        # update frame vars
        self.fx = self.display.frame.x
        self.fy = self.display.frame.y
        self.fw = self.display.frame.width
        self.fh = self.display.frame.height
        # dev mode
        self.developer = developer

        if self.state == 0:
            run = self.main_menu()
        elif self.state == 1:
            self.game()
        elif self.state == 2:
            self.levels()
        elif self.state == 3:
            self.options(events)

        return run, self.developer

    def main_menu(self):
        # background
        self.bg = pygame.transform.scale(self.fixed_bg, self.display.frame.size)
        # buttons
        self.buttons = []
        font_size = int(0.04 * self.fh)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        h = 0.072
        gap = 0.045
        width, height = 0.22 * self.fw, h * self.fh
        x = self.fx + 0.68 * self.fw
        rel_pos = []
        for i in range(4):
            rel_pos.append((x, self.fy + (0.36 + h / 2 + (h + gap) * i) * self.fh))
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
        # board
        width, height = 0.8 * self.fw, 0.8 * self.fh
        bg = pygame.transform.scale(pygame.image.load("assets/wave.png").convert_alpha(), (width, height))
        overlay = pygame.transform.scale(pygame.image.load("assets/overlay.jpg").convert_alpha(), (width, height))
        topleft = (self.fx + 0.1 * self.fw, self.fy + 0.1 * self.fh)
        bg_rect = bg.get_rect(topleft=topleft)
        overlay_rect = overlay.get_rect(topleft=topleft)

        # mask temp
        w, h = bg_rect.width, bg_rect.height
        temp_mask = pygame.surface.Surface((w - 0.1 * h, 0.9 * h))
        temp_mask.fill("black")
        overlay_with_mask = overlay.copy()
        overlay_with_mask.blit(temp_mask, (0.05 * h, 0.05 * h))
        overlay_with_mask.set_colorkey("black")

        # button
        font_size = int(0.04 * self.fh)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        x, y = self.fx + 0.5 * self.fw, self.fy + 0.95 * self.fh
        width = 0.22 * self.fw
        height = 0.072 * self.fh
        btn = Button(self.display.screen, "Main", "white", font, (x, y), self.button_img, width, height)

        # clicked
        if btn.clicked():
            self.state = 0

        # draw
        self.display.screen.blit(bg, bg_rect)
        self.display.screen.blit(overlay_with_mask, overlay_rect)
        btn.draw()

    def levels(self):
        # button
        font_size = int(0.04 * self.fh)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        x = self.fx + 0.5 * self.fw
        y = self.fy + 0.88 * self.fh
        width = 0.22 * self.fw
        height = 0.072 * self.fh
        btn = Button(self.display.screen, "Back", "white", font, (x, y), self.button_img, width, height)

        # draw
        btn.draw()

        # clicked
        if btn.clicked():
            self.state = 0

    def options(self, events):
        # layout
        row1_col1 = pygame.Rect(self.fx, self.fy + 0.10 * self.fh, self.fw/2, 0.15 * self.fh)
        row1_col2 = pygame.Rect(self.fx + self.fw/2, self.fy + 0.10 * self.fh, self.fw/2, 0.15 * self.fh)
        row2_col1 = pygame.Rect(self.fx, self.fy + 0.25 * self.fh, self.fw/2, 0.15 * self.fh)
        row2_col2 = pygame.Rect(self.fx + self.fw/2, self.fy + 0.25 * self.fh, self.fw/2, 0.15 * self.fh)
        row3_col1 = pygame.Rect(self.fx, self.fy + 0.40 * self.fh, self.fw/2, 0.15 * self.fh)
        row3_col2 = pygame.Rect(self.fx + self.fw/2, self.fy + 0.40 * self.fh, self.fw/2, 0.15 * self.fh)
        row4_col1 = pygame.Rect(self.fx, self.fy + 0.55 * self.fh, self.fw/2, 0.15 * self.fh)
        row4_col2 = pygame.Rect(self.fx + self.fw/2, self.fy + 0.55 * self.fh, self.fw/2, 0.15 * self.fh)

        # developer mode
        # -text
        font = pygame.font.SysFont("Ariel", round(0.06 * self.fh))
        text = font.render("Developer", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (row3_col1.right - 0.1*self.fw, row3_col1.center[1])
        # -switch
        pos = list(row3_col2.center)
        pos[0] = row3_col2.left + 0.1*self.fw
        switch = OnOff(self.display.screen, self.ON_img, self.OFF_img, 0.187 * self.fh, 0.08 * self.fh, pos, self.developer, events)
        self.developer = switch.if_clicked()

        # button
        font_size = int(0.04 * self.display.frame.height)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        x = self.fx + 0.5 * self.fw
        y = self.fy + 0.88 * self.fh
        width = 0.22 * self.fw
        height = 0.072 * self.fh
        btn = Button(self.display.screen, "Back", "white", font, (x, y), self.button_img, width, height)

        # clicked
        if btn.clicked():
            self.state = 0

        """
        # test
        board_rect = pygame.Rect(self.fx+0.3*self.fw / 2,  self.fy + 0.1 * self.fh / 2, 0.7 * self.fw, 0.7 * self.fh)
        self.scaled_bg = pygame.transform.scale(self.test, (0.7 * self.fw, 0.7 * self.fh))
        self.scaled_img = pygame.transform.scale(self.mask_img, (0.7 * self.fw, 0.7 * self.fh))
        self.scaled_bg.blit(self.scaled_img, (0, 0))
        self.scaled_bg.set_colorkey("black")"""

        # draw
        self.display.screen.blit(text, text_rect)
        switch.draw()
        btn.draw()
        # -layout
        if self.developer:
            pygame.draw.rect(self.display.screen, "#832222", row1_col1, 4)
            pygame.draw.rect(self.display.screen, "#421111", row1_col2, 4)
            pygame.draw.rect(self.display.screen, "#e0811b", row2_col1, 4)
            pygame.draw.rect(self.display.screen, "#9d5a13", row2_col2, 4)
            pygame.draw.rect(self.display.screen, "#f1db0b", row3_col1, 4)
            pygame.draw.rect(self.display.screen, "#a99908", row3_col2, 4)
            pygame.draw.rect(self.display.screen, "#51b12a", row4_col1, 4)
            pygame.draw.rect(self.display.screen, "#397c1d", row4_col2, 4)

        # self.display.screen.blit(self.scaled_bg, board_rect.topleft)

    def pause(self):
        pass
