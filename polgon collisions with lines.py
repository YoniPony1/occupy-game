import pygame

pygame.init()

# clock
clock = pygame.time.Clock()

# window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("polygon")

# polygon
polygon_points = [(150, 140), (150, 300), (450, 300), (450, 650), (600, 650), (600, 400), (950, 400), (950, 550),
                  (1150, 550), (1150, 260), (750, 260), (750, 140)]

# lines
lines = []
for i in range(len(polygon_points) - 1):
    lines.append([polygon_points[i], polygon_points[i + 1]])
lines.append([polygon_points[-1], polygon_points[0]])
vertical_lines = []
horizontal_lines = []

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
        vertical_lines.append(lines[ver_first + i])
        horizontal_lines.append(lines[hor_first + i])
print(vertical_lines)
print(horizontal_lines)

# ball
color = "red"
ball = pygame.Rect(100, 10, 50, 50)
direction = [-0.6, 0.8]
speed = 5


def collision():
    for line in horizontal_lines:
        x1, y1 = line[0][0], line[0][1]
        x2, y2 = line[1][0], line[1][1]
        # (x value)  if ball inside line or line inside ball
        if (x1 <= ball.left <= x2 or x2 <= ball.left <= x1) \
                or (x1 <= ball.right <= x2 or x2 <= ball.right <= x1) \
                or (ball.left <= x1 <= ball.right or ball.left <= x2 <= ball.right):
            # from top
            if abs(ball.bottom - y1) < speed:
                direction[1] *= -1
            # from bottom
            if abs(ball.top - y1) < speed:
                direction[1] *= -1

    for line in vertical_lines:
        x1, y1 = line[0][0], line[0][1]
        x2, y2 = line[1][0], line[1][1]
        # (y value)  if ball inside line or line inside ball
        if (y1 <= ball.top <= y2 or y2 <= ball.top <= y1) \
                or (y1 <= ball.bottom <= y2 or y2 <= ball.bottom <= y1) \
                or (ball.top <= y1 <= ball.bottom or ball.top <= y2 <= ball.bottom):
            # from left
            if abs(ball.right - x1) < speed:
                direction[0] *= -1
            # from right
            if abs(ball.left - x1) < speed:
                direction[0] *= -1


def move_ball():
    destination = (ball.x + speed * direction[0], ball.y + speed * direction[1])
    # checks if hit the edge
    if not 0 < destination[0] < width - ball.width:
        direction[0] *= -1
    if not 0 < destination[1] < height - ball.height:
        direction[1] *= -1
    destination = (ball.x + speed * direction[0], ball.y + speed * direction[1])
    # move ball
    ball.topleft = destination


# main loop
run = True
while run:
    # fps
    clock.tick(60)

    # ball movement
    move_ball()
    collision()
    # draw
    window.fill("orange")  # background
    pygame.draw.polygon(window, "white", polygon_points)  # polygon
    for line in lines:
        pygame.draw.line(window, "blue", line[0], line[1], 5)  # ----------- lines
    pygame.draw.rect(window, "red", ball)  # --------------------------- ball
    pygame.display.update()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
