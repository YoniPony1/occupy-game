import pygame

pygame.init()

# start window
monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
window_width = 0.7*monitor_width
window_height = 0.85*monitor_height
pygame.display.set_caption("game")
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()


def draw_rect():
    pygame.draw.rect(window, "red", rect)


# draw ui
def ui():
    pygame.Surface.fill(window, "#e6ccb3")

    # inside
    inside_width = round(0.8*window_width/20)*20  # make sure it's divided by 20
    inside_height = 0.7*inside_width
    inside_x, inside_y = (window_width-inside_width)/2, (window_height-inside_height)/2
    inside = pygame.Rect(inside_x, inside_y, inside_width, inside_height)
    pygame.draw.rect(window, "white", inside)
    inside_x_end, inside_y_end = inside_x+inside_width-1, inside_y+inside_height-1

    # outline
    outline_thick = 5
    outline_width = inside_width+outline_thick*2+1
    outline_height = inside_height+outline_thick*2+1
    outline_pos = (inside_x-1-outline_thick, inside_y-1-outline_thick)
    outline = pygame.Rect(outline_pos[0], outline_pos[1], outline_width, outline_height)
    pygame.draw.rect(window, "green", outline, outline_thick, 5)

    # guide lines
    color = "blue"
    gap = inside_width/20
    # vertical lines
    for i in range(1, 21):
        pygame.draw.line(window, color, (inside_x-1+gap*i, inside_y), (inside_x-1+gap*i, inside_y_end))
    # horizontal lines
    for j in range(1, 15):
        pygame.draw.line(window, color, (inside_x, inside_y-1+gap*j), (inside_x_end, inside_y-1+gap*j))
    pygame.draw.line(window, color, (inside_x-1, inside_y-1), (inside_x_end, inside_y-1))
    pygame.draw.line(window, color, (inside_x-1, inside_y-1), (inside_x-1, inside_y_end))

    # rect
    rect = pygame.Rect(inside_x_end-gap+1, inside_y_end-gap+1, gap-1, gap-1)

    return rect


def level_1():
    pass


# mainloop
def main():
    run = True
    while run:
        clock.tick(60)
        ui()
        draw_rect()
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect.x -= 5
        if keys[pygame.K_RIGHT]:
            rect.x += 5
        if keys[pygame.K_UP]:
            rect.y -= 5
        if keys[pygame.K_DOWN]:
            rect.y += 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


rect = ui()
main()

