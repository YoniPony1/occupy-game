import pygame
from display import Button
pygame.init()


class GameStates:
    def __init__(self, display):
        self.state = 0
        self.display = display

        # main_menu variables
        self.button_img = pygame.image.load("assets/orange_button.png").convert_alpha()
        self.buttons = []
        self.btns_args = {"play": {"text": "Play"},
                          "Levels": {"text": "Levels"},
                          "Settings": {"text": "Settings"},
                          "Quit": {"text": "Quit"}}
        color = "white"
        font_size = int(0.05 * self.display.frame.height)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        width, height = 0.26 * self.display.frame.width, 0.1 * self.display.frame.height
        h = 0.1
        gap = 0.04
        # first btn pos
        positions = [(self.display.frame.x + 0.5 * self.display.frame.width, self.display.frame.y + 0.29 * self.display.frame.height)]
        # adds all other btns pos
        for i in range(len(self.btns_args) - 1):
            positions.append((positions[i][0], positions[i][1] + (h + gap) * self.display.frame.height))

        j = 0
        for x in self.btns_args:
            self.btns_args[x]["pos"] = positions[j]
            self.buttons.append(Button(self.display.screen, self.btns_args[x]["text"], color, font,
                                       self.btns_args[x]["pos"], self.button_img, width, height))

            j += 1

    def states_manger(self, screen_scale):
        run = True
        s_w, s_h = screen_scale
        if self.state == 0:
            run = self.main_menu(s_w, s_h)
        elif self.state == 1:
            self.game()
        elif self.state == 2:
            self.levels()
        elif self.state == 3:
            self.options()

        return run

    def main_menu(self, w, h):
        # draw
        for x in self.buttons:
            x.draw()
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
        pass
