import pygame

pygame.init()


# button class
class Button:
    def __init__(self, surface, text, color, font, pos, image, width, height, align="center"):
        self.screen = surface
        self.image = pygame.transform.scale(image, (width, height))
        self.image_rect = self.image.get_rect()
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect()
        x, y = pos
        if align == "topleft":
            self.image_rect.topleft = (x, y)
            self.text_rect.topleft = (x, y)
        elif align == "center":
            self.image_rect.center = (x, y)
            self.text_rect.center = (x, y)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

    def draw(self):
        # draw button on screen
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.text, self.text_rect)


# display class
class Display:

    def __init__(self):
        # SCREEN INIT
        self.ratio = 3 / 2
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        monitor_ratio = self.monitor_width / self.monitor_height
        if monitor_ratio > self.ratio:
            screen_height = 0.85 * self.monitor_height
            screen_width = self.ratio * screen_height
        else:
            screen_width = 0.85 * self.monitor_width
            screen_height = (1 / self.ratio) * screen_width
        # screen
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        self.icon = pygame.image.load("assets/icon.png").convert_alpha()
        # icon
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("game")
        # background
        self.bg = pygame.transform.scale(pygame.image.load("assets/Purple_Background.png").convert_alpha(), self.screen.get_size())
        self.scaled_bg = self.bg.copy()
        # frame
        self.frame = pygame.Rect((0, 0), self.screen.get_size())
        # -------------

        # VARIABLES
        # fonts
        self.font = pygame.font.SysFont("Consolas", 0, bold=True)
        # fullscreen
        self.restore_down_size = self.screen.get_size()
        self.fullscreen = False
        # buttons
        self.btns_args = {}
        self.buttons = []
        # global
        # ------------

    def screen_resized(self, width, height):
        # UPDATE DISPLAY
        # adjust resolution
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.restore_down_size = (width, height)
        # adjust background
        self.scaled_bg = pygame.transform.scale(self.bg, self.screen.get_size())
        # adjust frame
        frame_ratio = self.ratio
        w, h = self.screen.get_size()
        if (w / h) > frame_ratio:
            frame_height = h
            frame_width = h * frame_ratio
            pos = ((w - frame_width) / 2, 0)
        else:
            frame_height = w / frame_ratio
            frame_width = w
            pos = (0, (h - frame_height) / 2)
        self.frame = pygame.Rect(pos, (frame_width, frame_height))

    def toggle_fullscreen(self, events):
        for event in events:
            # KEYS
            if event.type == pygame.KEYDOWN:
                # F clicked
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen  # toggle
                    if self.fullscreen:
                        # fullscreen on
                        self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height),
                                                              pygame.FULLSCREEN)
                        # update display
                        self.screen_resized(None, None)
                    else:
                        # fullscreen off
                        self.screen = pygame.display.set_mode(self.restore_down_size, pygame.RESIZABLE)

                # Esc clicked
                if event.key == pygame.K_ESCAPE:
                    if self.fullscreen:
                        # fullscreen off
                        self.fullscreen = False
                        self.screen = pygame.display.set_mode(self.restore_down_size, pygame.RESIZABLE)

    def set_main_menu(self):

        # buttons
        # -------
        color = "white"
        font_size = int(0.05 * self.frame.height)
        font = pygame.font.SysFont("Consolas", font_size, bold=True)
        width, height = 0.26 * self.frame.width, 0.1 * self.frame.height
        h = 0.1
        gap = 0.04

        # self.buttons["play"] = {"text": "Play", "color": None, "font": None, "pos": "",
        #                         "image": "", "width": "", "height": "", "align": "center"}
        # self.buttons["Levels"] = {"text": "Levels", "color": "", "font": "", "pos": "",
        #                           "image": "", "width": "", "height": "", "align": "center"}
        # self.buttons["Settings"] = {"text": "Settings", "color": "", "font": "", "pos": "",
        #                             "image": "", "width": "", "height": "", "align": "center"}
        # self.buttons["Quit"] = {"text": "Quit", "color": "", "font": "", "pos": "",
        #                         "image": "", "width": "", "height": "", "align": "center"}

        self.btns_args["play"] = {"text": "Play"}
        self.btns_args["Levels"] = {"text": "Levels"}
        self.btns_args["Settings"] = {"text": "Settings"}
        self.btns_args["Quit"] = {"text": "Quit"}

        positions = [(self.frame.x + 0.5 * self.frame.width, self.frame.y + 0.29 * self.frame.height)]
        for i in range(len(self.btns_args) - 1):
            positions.append((positions[i][0], positions[i][1] + (h + gap) * self.frame.height))
        j = 0
        self.buttons = []
        for x in self.btns_args:
            self.btns_args[x]["pos"] = positions[j]
            self.buttons.append(Button(self.screen, self.btns_args[x]["text"], color, font,
                                       self.btns_args[x]["pos"], self.button_img, width, height))
            self.buttons[j].draw()

            j += 1

        # if play_btn.clicked():
        #     self.main_menu = False
        #     self.game = True

    def draw(self):
        self.screen.blit(self.scaled_bg, (0, 0,))  # ----------- background
        pygame.draw.rect(self.screen, "red", self.frame, 2)  # frame

