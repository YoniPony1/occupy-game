import pygame

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

        # timer
        self.clock = pygame.time.Clock()
        # fonts
        self.big_font = pygame.font.SysFont("Ariel", 80)
        self.small_font = pygame.font.SysFont("Ariel", 40)
        # images
        self.backgroung = pygame.transform.scale(pygame.image.load("Background.png"),(self.window_width, self.window_height))
        self.button = pygame.image.load("orange_button.png")


        # vars
        self.rect_drawn = False
        self.in_field = False
        # pages vars
        self.main_menu = True
        self.game = False


    def draw_board(self):
        # board
        board_width = round(0.8*self.window_width/25)*25  # make sure it's divided by 20
        board_height = 0.68*board_width
        board_x, board_y = (self.window_width-board_width)/2, 0.35*(self.window_height-board_height)
        board = pygame.Rect(board_x, board_y, board_width, board_height)
        pygame.draw.rect(self.window, "#4a1486", board)
        board_x_end, board_y_end = board_x+board_width-1, board_y+board_height-1

        # outline
        outline_thick = 5
        outline_width = board_width+outline_thick*2+1
        outline_height = board_height+outline_thick*2+1
        outline_pos = (board_x-1-outline_thick, board_y-1-outline_thick)
        outline = pygame.Rect(outline_pos[0], outline_pos[1], outline_width, outline_height)
        pygame.draw.rect(self.window, "black", outline, outline_thick, 5)

        # guide lines
        #-------------
        color = "blue"
        gap = board_width/25
        # vertical lines
        for i in range(1, 26):
            pygame.draw.line(self.window, color, (board_x-1+gap*i, board_y), (board_x-1+gap*i, board_y_end))
        # horizontal lines
        for j in range(1, 18):
            pygame.draw.line(self.window, color, (board_x, board_y-1+gap*j), (board_x_end, board_y-1+gap*j))
        pygame.draw.line(self.window, color, (board_x-1, board_y-1), (board_x_end, board_y-1))
        pygame.draw.line(self.window, color, (board_x-1, board_y-1), (board_x-1, board_y_end))

        # background
        board_background = pygame.transform.scale(pygame.image.load("pattern2_21x17.png"), (board_width - 2 * gap-1, board_height - 2 * gap-1))
        self.window.blit(board_background, (board_x + gap, board_y + gap))

        #player
        if not self.rect_drawn:  # checks if it the first time its drawn
            #self.rect = pygame.Rect(board_x+12*gap, board_y_end - gap + 1, gap - 1, gap - 1)
            self.player = pygame.transform.scale(pygame.image.load("ball3.png"), (gap-1, gap-1))
            self.rect = self.player.get_rect()
            self.rect.topleft = (board_x+12*gap, board_y_end - gap + 1)
            self.rect_drawn = True
        self.window.blit(self.player, self.rect)

        #button
        button_1 = Button("Back", "white", self.small_font, self.window_width/2 , 0.936*self.window_height, self.button, 200, 60)
        button_1.draw()
        if button_1.clicked():
            self.main_menu = True
            self.game = False


    def draw_main_menu(self):
        play_btn = Button("Play", "white",self.big_font, self.window_width/2, 0.35*self.window_height, self.button, 380, 100)
        play_btn.draw()
        if play_btn.clicked():
            self.main_menu = False
            self.game = True


    def main_loop(self):
        run = True
        while run:
            velocity = 10

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
            if self.game:  # only when in game
                # arrow keys input
                if any((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
                    if keys[pygame.K_LEFT]:
                        direction = (-1, 0)
                    if keys[pygame.K_RIGHT]:
                        direction = (1, 0)
                    if keys[pygame.K_UP]:
                        direction = (0, -1)
                    if keys[pygame.K_DOWN]:
                        direction = (0, 1)

                    if self.in_field:
                        #mvement in the field
                        print(1)
                    else:
                        #movement in occupied area
                        print(0)
                        player_des = 0



            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


game = Game()
game.main_loop()
