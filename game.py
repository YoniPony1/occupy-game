import pygame

pygame.init()

# start window
monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
window_width = 0.7*monitor_width
window_height = 0.85*monitor_height
pygame.display.set_caption("game")
window = pygame.display.set_mode((window_width, window_height))


# draw ui
def draw():
    pygame.Surface.fill(window, "#e6ccb3")
    # outline
    outline_width = 0.8*window_width
    outline_height = 0.85*window_height
    outline_pos = ((window_width-outline_width)/2, (window_height-outline_height)/2)
    outline = pygame.Rect(outline_pos[0], outline_pos[1], outline_width, outline_height)
    outline_thick = 5
    pygame.draw.rect(window, "black", outline, outline_thick, 5)
    # inside
    inside_x, inside_y = outline_pos[0]+outline_thick, outline_pos[1]+outline_thick
    inside_width = outline_width-2*outline_thick
    inside_height = outline_height-2*outline_thick
    inside = pygame.Rect(inside_x, inside_y, inside_width, inside_height)
    pygame.draw.rect(window, "white", inside)
    inside_x_end, inside_y_end = inside_x+inside_width, inside_y+inside_height
    # guide lines
    gap = inside_width/20
    for i in range(20):
        pygame.draw.line(window, "orange", (inside_x+gap*i, inside_y), (inside_x+gap*i, inside_y_end))
    for j in range(int(inside_height/gap)+1):
        pygame.draw.line(window, "orange", (inside_x, inside_y+gap*j), (inside_x_end, inside_y+gap*j))
    # rect
    rect = pygame.Rect(inside_x_end-gap, inside_y_end-gap, gap, gap)
    pygame.draw.rect(window, "red", rect)

    pygame.display.update()


def level_1():
    pass


# mainloop
def main():
    run = True
    while run:
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
