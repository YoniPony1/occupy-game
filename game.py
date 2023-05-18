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


# ball class
class Ball():
    def __init__(self, image, size, start_pos, direction, speed):
        self.image = pygame.transform.scale(image, size)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = start_pos
        self.direction = direction
        self.speed = speed

    def draw(self):
        game.window.blit(self.image, self.image_rect)

    def move(self):
        (x, y) = self.image_rect.center
        (w, h) = self.image_rect[2:4]
        dest_x, dest_y= x+self.speed*self.direction[0], y+self.speed*self.direction[1]
        # checks if ball hits the wall
        hit_down, hit_up, hit_left, hit_right = False, False, False, False
        for area in game.field:
            if area[3] - h/2 <= dest_y and area[0] <= dest_x <= area[2]:
                hit_down = True
                dest_y = area[3] - h/2
            if area[1] + h/2 >= dest_y and area[0] <= dest_x <= area[2]:
                hit_up = True
                dest_y = area[1] + h/2
            if area[2] - w/2 <= dest_x and area[1] <= dest_y <= area[3]:
                hit_right = True
                dest_x = area[2] - w/2
            if area[0] + w/2 >= dest_x and area[1] <= dest_y <= area[3]:
                hit_left = True
                dest_x = area[0] + w/2
            text = f"dest_x: {dest_x}, edge: {area[0] + w/2}, {area[0] + w/2 >= dest_x}"

        if hit_down or hit_up:
            self.direction[1] *= -1
        if hit_right or hit_left:
            self.direction[0] *= -1

        self.image_rect.center = (dest_x, dest_y)


# main game class
class Game():
    def __init__(self):
        # start window
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        self.window_width = 0.7*self.monitor_width
        self.window_height = 0.85*self.monitor_height
        pygame.display.set_caption("game")
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        # sets max width
        if self.monitor_width/self.monitor_height > 1.78:
            self.max_width = (56/45)*self.monitor_height
            self.max_width_start = 0.5*(self.window_width-self.max_width)
        else:
            self.max_width = self.window_width
            self.max_width_start = 0

        # timer
        self.clock = pygame.time.Clock()
        # fonts
        self.big_font = pygame.font.SysFont("Ariel", int(0.8*0.055*self.max_width))
        self.small_font = pygame.font.SysFont("Ariel", int(0.8*0.033*self.max_width))
        # images
        self.background = pygame.transform.scale(pygame.image.load("Background2.png"), (self.window_width, self.window_height))
        self.button = pygame.image.load("orange_button.png")
        self.ball = pygame.image.load("ball5.png")

        # vars
        self.board_area = []
        self.player_drawn = False
        self.field_init = False
        self.ball_init = False
        self.p_velocity = 0.2*round(0.8*self.max_width/25)
        self.in_field = False
        self.field = []
        self.points = []
        self.direction = (0, 0)
        self.fixed_direction = (0, 0)
        self.polygons= []
        # pages vars
        self.main_menu = True
        self.game = False

    def draw_board(self):
        # board
        board_width = round(0.8*self.max_width/25)*25  # make sure it's divided by 25
        board_height = round(0.68*board_width)
        board_x, board_y = round((self.max_width-board_width)/2+self.max_width_start), round((self.window_height-1.12*board_height)/2 - 0.5*round(0.0051*board_height))
        board = pygame.Rect(board_x, board_y, board_width, board_height)
        pygame.draw.rect(self.window, "#4a1486", board)
        board_x_end, board_y_end = board_x+board_width-1, board_y+board_height-1
        self.board_area = [board_x, board_y, board_x + board_width - 1, board_y + board_height - 1]

        # outline
        outline_thick = round(0.0051*board_height)
        outline_width = board_width+outline_thick*2+1
        outline_height = board_height+outline_thick*2+1
        outline_pos = (board_x-1-outline_thick, board_y-1-outline_thick)
        outline = pygame.Rect(outline_pos[0], outline_pos[1], outline_width, outline_height)
        pygame.draw.rect(self.window, "black", outline, outline_thick, 5)

        # guide lines
        # -------------
        color = "white"
        gap = board_width/25
        # vertical lines
        for i in range(1, 26):
            pygame.draw.line(self.window, color, (board_x-1+gap*i, board_y), (board_x-1+gap*i, board_y_end))
        # horizontal lines
        for j in range(1, 18):
            pygame.draw.line(self.window, color, (board_x, board_y-1+gap*j), (board_x_end, board_y-1+gap*j))
        # 2 edge lines
        pygame.draw.line(self.window, color, (board_x-1, board_y-1), (board_x_end, board_y-1))
        pygame.draw.line(self.window, color, (board_x-1, board_y-1), (board_x-1, board_y_end))

        # field
        field_background = pygame.transform.scale(pygame.image.load("pattern2_21x17.png"), (board_width - 2 * gap-1, board_height - 2 * gap-1))
        self.window.blit(field_background, (board_x + gap, board_y + gap))
        if not self.field_init:
            self.field.append((board_x + gap, board_y + gap, board_x + board_width - gap - 2, board_y + board_height - gap - 2))
            self.field_init = True

        # player
        if not self.player_drawn:  # checks if it is the first time its drawn
            self.player = pygame.transform.scale(pygame.image.load("ball3.png"), (gap-1, gap-1))
            self.player_rect = self.player.get_rect()
            self.player_rect.topleft = (board_x+12*gap, board_y_end - gap + 1)
            self.player_drawn = True
        self.window.blit(self.player, self.player_rect)
        pygame.draw.rect(self.window, "red", self.player_rect, 1)

        # back button
        self.back_button = Button("Back", "white", self.small_font, 0.5*self.max_width+self.max_width_start, board_y+1.09*outline_height, self.button, 0.2*outline_height, 0.06*outline_height)
        self.back_button.draw()

    def balls(self):
        ball1_size = round(0.8 * self.max_width / 25) - 1
        if not self.ball_init:  # only when it is the first time (initiate)
            self.ball1 = Ball(self.ball, (ball1_size, ball1_size), (400, 200), [0.5, 1], 10)
            self.ball2 = Ball(self.ball, (ball1_size, ball1_size), (700, 500), [-1, -0.35], 10)
            self.ball_init = True
        self.ball1.draw()
        self.ball2.draw()
        self.ball1.move()
        self.ball2.move()

    def draw_occupied_area(self):
        # occupied area
        for polygon in self.polygons:
            pygame.draw.polygon(self.window, "#4a1486", polygon)

    def back_button_clicked(self):
        if self.back_button.clicked():
            self.main_menu = True
            self.game = False
            # reset vars
            self.player_drawn = False
            self.in_field = False
            self.field = []
            self.points = []
            self.field_init = False
            self.ball_init = False

    def draw_main_menu(self):
        play_btn = Button("Play", "white", self.big_font, 0.5*self.max_width+self.max_width_start, 0.35*self.window_height, self.button, 0.212*self.max_width, 0.055*self.max_width)
        play_btn.draw()
        if play_btn.clicked():
            self.main_menu = False
            self.game = True

    def arrow_key_pressed(self):
        if self.in_field:
            # player inside field
            # -------------------
            # check if changed direction
            if self.direction != self.fixed_direction:
                # adds point
                point = self.player_rect.center
                self.points.append(point)
                self.fixed_direction = self.direction
                print("changed direction")
        else:
            # player outside field
            # --------------------
            player_des_x = self.player_rect.x + self.p_velocity * self.direction[0]
            player_des_y = self.player_rect.y + self.p_velocity * self.direction[1]
            # limits to the board area
            if player_des_x > (self.board_area[2] - self.player_rect[2]):
                player_des_x = (self.board_area[2] - self.player_rect[2])
            elif player_des_x < self.board_area[0]:
                player_des_x = self.board_area[0]
            if player_des_y > (self.board_area[3] - self.player_rect[3]):
                player_des_y = (self.board_area[3] - self.player_rect[3])
            elif player_des_y < self.board_area[1]:
                player_des_y = self.board_area[1]

            # check if player destination is in field
            for area in self.field:
                if area[2] >= player_des_x >= (area[0] - self.player_rect[2]) and \
                        area[3] >= player_des_y >= (area[1] - self.player_rect[3]):
                    self.in_field = True
                    self.fixed_direction = self.direction
                    # adds start point
                    point = self.player_rect.center
                    self.points.append(point)

            # moves player
            self.player_rect.x = player_des_x
            self.player_rect.y = player_des_y

    def in_field_move(self):
        # calculate player destination
        player_des_x = self.player_rect.x + self.p_velocity * self.fixed_direction[0]
        player_des_y = self.player_rect.y + self.p_velocity * self.fixed_direction[1]
        # if in field
        in_area = []
        for area in self.field:  # checks if player in field
            if area[2] >= self.player_rect.x >= (area[0] - self.player_rect[2]) and \
                    area[3] >= self.player_rect.y >= (area[1] - self.player_rect[3]):
                in_area.append(True)
                # limits to the board area
                if player_des_x > (self.board_area[2] - self.player_rect[2]):
                    player_des_x = (self.board_area[2] - self.player_rect[2])
                elif player_des_x < self.board_area[0]:
                    player_des_x = self.board_area[0]
                if player_des_y > (self.board_area[3] - self.player_rect[3]):
                    player_des_y = (self.board_area[3] - self.player_rect[3])
                elif player_des_y < self.board_area[1]:
                    player_des_y = self.board_area[1]
                # moves player
                self.player_rect.x = player_des_x
                self.player_rect.y = player_des_y
            else:
                in_area.append(False)
        # if not in field
        if not all(in_area):
            self.in_field = False
            # adds end point
            point = self.player_rect.center
            self.points.append(point)
            # filling the area
            self.polygons.append(self.points)
            # reset points
            self.points = []

    def draw_lines(self):
        if self.in_field:
            pygame.draw.line(self.window, "white", self.player_rect.center, self.points[-1], 10)

            for i in range(len(self.points)-1):
                pygame.draw.line(self.window, "white", self.points[i], self.points[i+1], 10)

    def main_loop(self):
        run = True
        while run:
            # clock
            self.clock.tick(60)

            # draw
            self.window.blit(self.background, (0, 0))
            if self.main_menu:
                self.draw_main_menu()
            elif self.game:
                self.draw_board()
                self.draw_lines()
                self.balls()
                self.draw_occupied_area()
                self.back_button_clicked()
            pygame.display.update()

            #  game arrow keys input
            if self.game:  # only when in game
                keys = pygame.key.get_pressed()
                if any((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
                    if keys[pygame.K_LEFT]:
                        self.direction = (-1, 0)
                    elif keys[pygame.K_RIGHT]:
                        self.direction = (1, 0)
                    elif keys[pygame.K_UP]:
                        self.direction = (0, -1)
                    elif keys[pygame.K_DOWN]:
                        self.direction = (0, 1)
                    # calls function
                    self.arrow_key_pressed()

            # field movement
            if self.game:
                if self.in_field:
                    self.in_field_move()

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False


game = Game()
game.main_loop()
pygame.quit()
