import pytest
import pygame
from organized.display import Button

pygame.init()
surface = pygame.Surface((500, 500))
text = "click me"
color = "black"
font = pygame.font.SysFont("Ariel", 50)
pos = [0, 0]
image = pygame.Surface((200, 200))
image.fill("red")
width, height = 200, 200


def test_button_class():
    btn = Button(surface, text, color, font, pos, image, width, height)
    assert btn != 0
