import pygame

pygame.init()


# text class
class Text:
    def __init__(self, surface, pos, text, color, font_family, font_size, bold=False):
        font = pygame.font.SysFont(font_family, font_size, bold=bold)
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pos
        self.surface = surface

    def draw(self):
        self.surface.blit(self.text, self.text_rect)


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


# on-off switch class
class OnOff:
    def __init__(self, surface, on_img, off_img, width, height, pos, if_on, events):
        self.screen = surface
        self.ON = pygame.transform.scale(on_img, (width, height))
        self.OFF = pygame.transform.scale(off_img, (width, height))
        self.rect = self.ON.get_rect()
        self.rect.center = pos
        self.if_on = if_on
        self.events = events

    def draw(self):
        if self.if_on:
            self.screen.blit(self.ON, self.rect)
        else:
            self.screen.blit(self.OFF, self.rect)

    def if_clicked(self):
        pos = pygame.mouse.get_pos()
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:

                if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pos):
                    return not self.if_on
        return self.if_on


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

    def draw(self):
        self.screen.blit(self.scaled_bg, (0, 0,))  # ----------- background
        pygame.draw.rect(self.screen, "red", self.frame, 2)  # frame
