import pygame
import random
pygame.init()


# field object
class Field:
    def __init__(self, points):
        # POINTS
        # list of all filed points in x,y tuples
        # [(x1, y1), (x2, y2), (x3, y3)....]
        self.points = points
        # LINES
        # list of all field lines. each line is a list of 2 points
        # [[(x1,y1), (x2,y2)], [(x1,y1), (x2,y2)], [(x1,y1), (x2,y2)]...]
        self.lines = self.lines()
        # vertical lines
        self.ver_lines = self.vertical_lines()
        # horizontal lines
        self.hor_lines = self.horizontal_lines()

    def lines(self):
        lines = []
        for i in range(len(self.points) - 1):
            lines.append([self.points[i], self.points[i+1]])
        lines.append([self.points[-1], self.points[0]])
        return lines

    def vertical_lines(self):
        ver_lines = []
        if self.lines[0][0][0] == self.lines[0][1][0]:
            # first line is vertical
            first_line = 0
        else:
            # first line is horizontal
            first_line = 1
        for i in range(len(self.lines)//2):
            ver_lines.append(self.lines[first_line+2*i])

        return ver_lines

    def horizontal_lines(self):
        hor_lines = []
        if self.lines[0][0][1] == self.lines[0][1][1]:
            # first line is horizontal
            first_line = 0
        else:
            # first line is vertical
            first_line = 1
        for i in range(len(self.lines)//2):
            hor_lines.append(self.lines[first_line+2*i])

        return hor_lines


class Logic:
    def __init__(self):
        pass

    def if_in_field(self, point, vertical_lines):
        # if a point is inside field
        point = point
        ver_lines = vertical_lines
        # how many lines have the same y value of the point
        count = 0
        for line in ver_lines:
            y1, y2 = line[0][1], line[1][1]
            x1 = line[0][0]
            if min(y1, y2) < point[1] < max(y1, y2) and point[0] < x1:
                count += 1

        print(count)


class Gui:
    def __init__(self):
        WIDTH = 1920
        HEIGHT = 1080
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Field
        points = []
        points_num = random.randrange(4, 21, 2)
        last = [random.randrange(100, 1800), random.randrange(100, 900)]
        for i in range(points_num-1):
            point = [0, 0]
            if i % 2 == 0:
                point[0] = random.randrange(100, 1800)
                point[1] = last[1]
            else:
                point[0] = last[0]
                point[1] = random.randrange(100, 900)
            points.append(point)
            last = point
        points.append([last[0], points[0][1]])
        # points = [(300, 200), (300, 400), (400, 400), (400, 200), (480, 200), (480, 100), (100, 100), (100, 200)]
        self.field = Field(points)

        # logic
        self.point = (500, 300)
        logic = Logic()
        logic.if_in_field(self.point, self.field.ver_lines)

    def draw_shape(self):
        for line in self.field.lines:
            pygame.draw.line(self.screen, "green", line[0], line[1], 4)
        i = 0
        for point in self.field.points:
            i += 1
            pygame.draw.circle(self.screen, "blue", point, 5)
            font = pygame.font.SysFont("Ariel", 18)
            text = font.render(str(point), True, "black")
            num = font.render(str(i), True, "Black")
            self.screen.blit(text, (point[0] - 30, point[1]-20))
            self.screen.blit(num, (point[0] - 10, point[1] - 33))


    def main_loop(self):
        run = True
        while run:

            # draw
            self.screen.fill("gray")
            self.draw_shape()
            pygame.draw.circle(self.screen, "red", self.point, 5)

            pygame.display.update()

            # quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


try1 = Gui()
try1.main_loop()
