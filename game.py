import pygame

pygame.init()


# button class
class Button:
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
class Ball:
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
class Game:
    def __init__(self):
        # start window
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        self.window_width = 0.7*self.monitor_width
        self.window_height = 0.85*self.monitor_height
        pygame.display.set_caption("game")
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        print(f"monitor: {self.monitor_width}, {self.monitor_height}")
        print(f"og board size: {1425}, {969}")
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
        self.board_size = []
        self.board_area = []
        self.player_drawn = False
        self.field_init = False
        self.ball_init = False
        self.p_velocity = 0.2*round(0.8*self.max_width/25)
        self.in_field = False
        self.field = []
        self.field_points = []
        self.points = []
        self.direction = (0, 0)
        self.fixed_direction = (0, 0)
        self.polygons = []
        # pages vars
        self.main_menu = True
        self.game = False

    def draw_main_menu(self):
        play_btn = Button("Play", "white", self.big_font, 0.5 * self.max_width + self.max_width_start,
                          0.35 * self.window_height, self.button, 0.212 * self.max_width, 0.055 * self.max_width)
        play_btn.draw()
        if play_btn.clicked():
            self.main_menu = False
            self.game = True

    def draw_board(self):
        # board
        board_width = round(0.8*self.max_width/25)*25  # make sure it's divided by 25
        board_height = round(0.68*board_width)
        board_x, board_y = round((self.max_width-board_width)/2+self.max_width_start), round((self.window_height-1.12*board_height)/2 - 0.5*round(0.0051*board_height))
        board = pygame.Rect(board_x, board_y, board_width, board_height)
        pygame.draw.rect(self.window, "#4a1486", board)
        board_x_end, board_y_end = board_x+board_width-1, board_y+board_height-1
        self.board_area = [board_x, board_y, board_x + board_width - 1, board_y + board_height - 1]
        self.board_size = [board_width, board_height]

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
            x1, y1, x2, y2 = board_x + gap, board_y + gap, board_x + board_width - gap - 2, board_y + board_height - gap - 2
            self.field.append((x1, y1, x2, y2))
            self.field_points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            self.field_lines()
            self.field_init = True
            self.field_surface = pygame.Surface((x2-x1+1, y2-y1+1))
            self.field_surface.fill("red")
            self.field_mask = pygame.mask.from_surface(self.field_surface)
            self.maskimg = self.field_mask.to_surface()
            self.field_rect = self.field_surface.get_rect()
            self.field_rect.topleft = (x1, y1)

        # player
        if not self.player_drawn:  # checks if it is the first time its drawn
            self.player = pygame.transform.scale(pygame.image.load("ball3.png"), (gap-1, gap-1))
            self.player_drawn = True
            self.player_surface = pygame.Surface((gap-1, gap-1), pygame.SRCALPHA)
            self.player_surface.blit(self.player, (0, 0))
            self.player_rect = self.player_surface.get_rect()
            self.player_rect.topleft = (board_x+12*gap, board_y_end - gap + 1)
            pygame.display.update()
            self.player_mask = pygame.mask.from_surface(self.player_surface)
            self.maskimg2 = self.player_mask.to_surface()

        # back button
        self.back_button = Button("Back", "white", self.small_font, 0.5*self.max_width+self.max_width_start, board_y+1.09*outline_height, self.button, 0.2*outline_height, 0.06*outline_height)
        self.back_button.draw()

    def draw_lines(self):
        if self.in_field:
            if self.direction[0] > 0:  # right
                p_point = self.player_rect.midleft
            elif self.direction[0] < 0:  # left
                p_point = self.player_rect.midright
            elif self.direction[1] > 0:  # down
                p_point = self.player_rect.midtop
            else:  # up
                p_point = self.player_rect.midbottom
            pygame.draw.line(self.window, "white", p_point, self.points[-1], round(0.007 * self.board_size[0]))
            for i in range(len(self.points) - 1):
                pygame.draw.line(self.window, "white", self.points[i], self.points[i + 1],
                                 round(0.007 * self.board_size[0]))

    def balls(self):
        ball1_size = self.board_size[0]/25 - 1
        if not self.ball_init:  # only when it is the first time (initiate)
            self.ball1 = Ball(self.ball, (ball1_size, ball1_size), (0.3*self.board_size[0], 0.14*self.board_size[0]), [0.5, 1], 0.007*self.board_size[0])
            self.ball2 = Ball(self.ball, (ball1_size, ball1_size), (0.5*self.board_size[0], 0.35*self.board_size[0]), [-1, -0.35], 0.007*self.board_size[0])
            self.ball_init = True
        self.ball1.draw()
        self.ball2.draw()
        self.ball1.move()
        self.ball2.move()

    def draw_occupied_area(self):
        # occupied area
        for polygon in self.polygons:
            if len(polygon) > 2:
                pygame.draw.polygon(self.window, "#4a1486", polygon)

    def occupying_area(self):
        start = self.points[0]
        end = self.points[-1]
        # check where is the end point, in field_points list
        for i in range(len(self.field_points)):
            point1 = self.field_points[i]
            if i+1 == len(self.field_points):
                point2 = self.field_points[0]
            else:
                point2 = self.field_points[i+1]
            # the same x (horizontal)
            if end[0] == point1[0] and point1[1] <= end[1] <= point2[1]:
                print(True)

        print(self.field_points)
        print(self.points)

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
            self.polygons = []

    def draw_player(self):
        self.window.blit(self.player_surface, self.player_rect)
        pygame.draw.rect(self.window, "red", self.player_rect, 1)

    def field_lines(self):
        lines = []
        for i in range(len(self.field_points) - 1):
            lines.append([self.field_points[i], self.field_points[i + 1]])
        lines.append([self.field_points[-1], self.field_points[0]])
        self.vertical_lines = []
        self.horizontal_lines = []
        if lines[0][0][0] == lines[0][1][0]:
            # first line is vertical
            ver_first = 0
            hor_first = 1
        else:
            # first line is horizontal
            ver_first = 1
            hor_first = 0
        for i in range(0, len(lines) + 1, 2):
            # i = (0,2,4,6,8.....)
            if ver_first + i < len(lines) and hor_first + i < len(lines):
                self.vertical_lines.append(lines[ver_first + i])
                self.horizontal_lines.append(lines[hor_first + i])
        print(self.vertical_lines)
        print(self.horizontal_lines)

    def check_if_in_field(self, rect, speed, direction):
        rect = rect
        speed = speed
        direction = direction
        for line in self.horizontal_lines:
            x1, y1 = line[0][0], line[0][1]
            x2, y2 = line[1][0], line[1][1]
            # (x value)  if rect inside line or line inside ball
            if (x1 <= rect.left <= x2 or x2 <= rect.left <= x1) \
                    or (x1 <= rect.right <= x2 or x2 <= rect.right <= x1) \
                    or (rect.left <= x1 <= rect.right or rect.left <= x2 <= rect.right):
                # from top
                if abs(rect.bottom - y1) <= speed and direction[1] > 0:
                    return "top"
                # from bottom
                if abs(rect.top - y1) <= speed and direction[1] < 0:
                    return "bottom"

        for line in self.vertical_lines:
            x1, y1 = line[0][0], line[0][1]
            x2, y2 = line[1][0], line[1][1]
            # (y value)  if rect inside line or line inside ball
            if (y1 <= rect.top <= y2 or y2 <= rect.top <= y1) \
                    or (y1 <= rect.bottom <= y2 or y2 <= rect.bottom <= y1) \
                    or (rect.top <= y1 <= rect.bottom or rect.top <= y2 <= rect.bottom):
                # from left
                if abs(rect.right - x1) <= speed and direction[0] > 0:
                    return "left"
                # from right
                if abs(rect.left - x1) <= speed and direction[0] < 0:
                    return "right"

    def arrow_key_pressed(self):
        player_des_x = self.player_rect.x + self.p_velocity * self.direction[0]
        player_des_y = self.player_rect.y + self.p_velocity * self.direction[1]

        if self.in_field:
            # player inside field
            # -------------------
            # check if changed direction (not accepting going back, only to the sides)
            if self.direction != self.fixed_direction and self.direction != (-self.fixed_direction[0], -self.fixed_direction[1] ):
                # adds point
                point = self.player_rect.center
                self.points.append(point)
                self.fixed_direction = self.direction
        else:
            # player outside field
            # --------------------
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
                    point = list(self.player_rect.center)
                    point[0] += (self.direction[0] * round(0.8*self.max_width/25))//2
                    point[1] += (self.direction[1] * round(0.8*self.max_width/25))//2
                    self.points.append(tuple(point))

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
            point = list(self.player_rect.center)
            point[0] += -(self.direction[0]*(round(0.8*self.max_width/25)))//2
            point[1] += -(self.direction[1]*(round(0.8*self.max_width/25)))//2
            self.points.append(tuple(point))
            # filling the area
            self.occupying_area()
            self.polygons.append(self.points)
            # reset points
            self.points = []

    def main_loop(self):
        run = True
        while run:
            # clock
            self.clock.tick(60)

            # arrow keys input
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

            # player field movement
            if self.game:
                if self.in_field:
                    self.in_field_move()

            # draw
            self.window.blit(self.background, (0, 0))
            if self.main_menu:
                self.draw_main_menu()
            elif self.game:
                self.draw_board()
                self.draw_lines()
                self.balls()
                self.draw_occupied_area()
                self.draw_player()

                # testing
                pygame.draw.circle(self.window, "red", self.field_rect.topleft, 5)
                pygame.draw.circle(self.window, "red", self.player_rect.topleft, 5)
                pygame.draw.circle(self.window, "blue", (self.field_rect.x + 638, self.field_rect.y + 849), 5)

                # back button reset
                self.back_button_clicked()
            pygame.display.update()

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
