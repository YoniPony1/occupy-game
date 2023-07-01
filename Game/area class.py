import pygame
pygame.init()


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

    def lines(self):
        lines = []
        for i in range(len(self.points) - 1):
            lines.append([self.points[i], self.points[i+1]])
        lines.append([self.points[-1], self.points[0]])
        return lines

    def vertical_lines(self):
        ver_lines = []
        if self.lines[0][0][1] == self.lines[0][1][1]:
            # first line is vertical
            first_line = 0
        else:
            # first line is horizontal
            first_line = 1
        for i in range(len(self.lines)//2):
            ver_lines.append(self.lines[first_line+2*i])

        return ver_lines

