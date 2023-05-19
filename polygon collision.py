import pygame

pygame.init()

# clock
clock = pygame.time.Clock()

# window
width, height = 1920, 1080
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("polygon")

# polygon
polygon_surface = pygame.Surface((300, 600), pygame.SRCALPHA)
polygon_points = [(100, 100), (220, 100), (220, 280), (400, 280), (400, 700), (60, 700), (60, 400), (200, 400), (200, 350), (100, 350)]
polygon_points_offset = [(point[0]-60, point[1]-100) for point in polygon_points]
polygon = pygame.draw.polygon(polygon_surface, "white", polygon_points_offset)
polygon_mask = pygame.mask.from_surface(polygon_surface)
mask_image = polygon_mask.to_surface()
polygon_surface_pos = (60, 100)

# ball
ball_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
ball_surface.fill("black")
direction = [1, -0.8]
speed = 4
ball_mask = pygame.mask.from_surface(ball_surface)
ball_surface_rect = ball_surface.get_rect()
ball_surface_rect.topleft = (400, 600)


def check_for_collision():
    destination = (ball_surface_rect.x + speed * direction[0], ball_surface_rect.y + speed * direction[1])

    if polygon_mask.overlap(ball_mask, (destination[0] - polygon_surface_pos[0], destination[1] - polygon_surface_pos[1])):
        color = "green"
        print(ball_mask.overlap(polygon_mask, (polygon_surface_pos[0] - destination[0], polygon_surface_pos[1] - destination[1] )))
    else:
        color = "red"
    return color


def move_ball():
    destination = (ball_surface_rect.x + speed * direction[0], ball_surface_rect.y + speed * direction[1])
    # checks if hit the edge
    if not 0 < destination[0] < width-ball_surface_rect.width:
        direction[0] *= -1
    if not 0 < destination[1] < height-ball_surface_rect.height:
        direction[1] *= -1

    # move ball
    ball_surface_rect.topleft = destination


# main loop
run = True
while run:
    # fps
    clock.tick(60)

    # ball movement
    color = check_for_collision()
    move_ball()

    # draw
    window.fill("orange")
    window.blit(polygon_surface, polygon_surface_pos)
    ball_surface.fill(color)
    window.blit(ball_surface, ball_surface_rect)
    pygame.display.update()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

