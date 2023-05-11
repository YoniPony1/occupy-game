import pygame
import button

pygame.init()

# button class
class Button():
    def __init__(self, text, color, font, x, y, image, width, height, align = "center"):
        self.image = pygame.transform.scale(image, (width, height))
        self.image_rect = self.image.get_rect()
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect()
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
        game.window.blit(self.image, self.image_rect)
        game.window.blit(self.text, self.text_rect)

#maingame class
class Game():
    def __init__(self):
        # start window
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        self.window_width = 0.7*self.monitor_width
        self.window_height = 0.85*self.monitor_height
        pygame.display.set_caption("game")
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        self.rect_drawn = False

        # timer
        self.clock = pygame.time.Clock()
        # fonts
        self.big_font = pygame.font.SysFont("Ariel", 80)
        self.small_font = pygame.font.SysFont("Ariel", 40)
        # images
        self.backgroung = pygame.transform.scale(pygame.image.load("Background.png"),(self.window_width, self.window_height))
        self.img = pygame.image.load("orange_button.png")

        # pages vars
        self.main_menu = True
        self.board = False


    def draw_board(self):
        # inside
        inside_width = round(0.8*self.window_width/20)*20  # make sure it's divided by 20
        inside_height = 0.7*inside_width
        inside_x, inside_y = (self.window_width-inside_width)/2, 0.35*(self.window_height-inside_height)
        inside = pygame.Rect(inside_x, inside_y, inside_width, inside_height)
        pygame.draw.rect(self.window, "white", inside)
        inside_x_end, inside_y_end = inside_x+inside_width-1, inside_y+inside_height-1

        # outline
        outline_thick = 5
        outline_width = inside_width+outline_thick*2+1
        outline_height = inside_height+outline_thick*2+1
        outline_pos = (inside_x-1-outline_thick, inside_y-1-outline_thick)
        outline = pygame.Rect(outline_pos[0], outline_pos[1], outline_width, outline_height)
        pygame.draw.rect(self.window, "green", outline, outline_thick, 5)

        # guide lines
        #-------------
        color = "blue"
        gap = inside_width/20
        # vertical lines
        for i in range(1, 21):
            pygame.draw.line(self.window, color, (inside_x-1+gap*i, inside_y), (inside_x-1+gap*i, inside_y_end))
        # horizontal lines
        for j in range(1, 15):
            pygame.draw.line(self.window, color, (inside_x, inside_y-1+gap*j), (inside_x_end, inside_y-1+gap*j))
        pygame.draw.line(self.window, color, (inside_x-1, inside_y-1), (inside_x_end, inside_y-1))
        pygame.draw.line(self.window, color, (inside_x-1, inside_y-1), (inside_x-1, inside_y_end))

        #rect
        if not self.rect_drawn:  # checks if it the first time
            self.rect = pygame.Rect(inside_x_end - gap + 1, inside_y_end - gap + 1, gap - 1, gap - 1)
            self.rect_drawn = True
        pygame.draw.rect(self.window, "red", self.rect)

        #button
        button_1 = Button("Back", "white", self.small_font, self.window_width/2 , 0.945*self.window_height, self.img, 200, 60)
        button_1.draw()
        if button_1.clicked():
            self.main_menu = True
            self.board = False


    def draw_main_menu(self):
        play_btn = Button("Play", "white",self.big_font, self.window_width/2, 0.35*self.window_height, self.img, 380, 100)
        play_btn.draw()
        if play_btn.clicked():
            self.main_menu = False
            self.board = True


    def main_loop(self):
        run = True
        while run:
            #clock
            self.clock.tick(60)

            #draw
            self.window.blit(self.backgroung, (0, 0))
            if self.main_menu:
                self.draw_main_menu()
            else:
                self.draw_board()
            pygame.display.update()

            #key inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False



game = Game()
game.main_loop()
