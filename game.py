from typing import Any
import pygame
from sys import exit

pygame.init()

# Set up of game window
screen = pygame.display.set_mode((800,700))
pygame.display.set_caption('Escaping Big Brother')
programIcon = pygame.image.load('1984-bbimg.jpeg').convert()
pygame.display.set_icon(programIcon)

class Eye():
    def __init__(self, x_pos, y_pos) -> None:
        self.img = pygame.image.load('falling_objects/eye.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.x_pos = x_pos
        self.y_pos = y_pos

class Book():
    def __init__(self, x_pos, y_pos) -> None:
        self.img = pygame.image.load("falling_objects/book.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (160,120))
        self.x_pos = x_pos
        self.y_pos = y_pos

class Player():
    def __init__(self, x_pos) -> None:
        self.img = pygame.image.load("box.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (200,200))
        self.x_pos = x_pos
        self.score = 0

    def increase_score(self):
        self.score += 1


# Getting background images loaded into variables
background = pygame.image.load('cityscape.png').convert()
floor_background = pygame.Surface((800, 50))
floor_background.fill("#310108")
sky_background = pygame.Surface((800,300))
sky_background.fill("#8a041b")


clock = pygame.time.Clock()
player_x_pos = 400
player_y_pos = 530

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Setting background images on screen
    screen.blit(sky_background, (0,0))
    screen.blit(background, (0,300))
    screen.blit(floor_background, (0, 650))

    a = Eye(10,10)
    screen.blit(a.img, (a.x_pos, a.y_pos))
    #screen.blit(book, (150,50))

    player = Player(player_x_pos)
    if player_x_pos >= 850:
        player_x_pos = -100
    else:
        screen.blit(player.img, (player.x_pos, player_y_pos))
        player_x_pos += 1
    
    pygame.display.update()
    clock.tick(120)
