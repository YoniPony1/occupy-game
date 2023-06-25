import pygame
from display import Display
from game_states import GameStates

pygame.init()


class Main:
    def __init__(self):
        # timer
        self.clock = pygame.time.Clock()

        # calls classes
        self.display = Display()
        self.states = GameStates(self.display)

    def main_loop(self):
        run = True
        while run:
            # events
            events = pygame.event.get()

            # frames per sec
            self.clock.tick(60)

            # draw display
            self.display.toggle_fullscreen(events)
            self.display.draw()

            # game states
            run = self.states.states_manger()

            pygame.display.update()

            # events
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                # resize display
                if event.type == pygame.VIDEORESIZE:
                    self.display.screen_resized(event.w, event.h)

        pygame.quit()


if __name__ == '__main__':
    game = Main()
    game.main_loop()
