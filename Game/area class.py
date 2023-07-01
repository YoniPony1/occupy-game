import pygame

pygame.init()


class Area:
    def __init__(self, board_frame):
        # board variables
        self.bx = board_frame.x
        self.by = board_frame.y
        self.bw = board_frame.width
        self.bh = board_frame.height
        # area rectangle
        y = self.by + 0.05 * self.bh
        x = self.bx + y
        height = 0.9 * self.bh
        width = self.bw - 2 * (x - self.bx)
        self.area_rect = pygame.Rect(x, y, width, height)
        # 4 default points
        self.default = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]

        self.points = []


area = Area(pygame.Rect(0, 0, 0, 0))
