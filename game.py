from typing import Any
import pygame
from sys import exit

pygame.init()

# Set up of game window
WINDOW_X = 800
WINDOW_Y = 700
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('Escaping Big Brother')
programIcon = pygame.image.load('1984-bbimg.jpeg').convert()
pygame.display.set_icon(programIcon)
my_font = pygame.font.SysFont('Arial', 15)

# Represents a falling object (object the player either avoids or tries to obtain)
class FallingObject():
    def __init__(self, x_pos, y_pos) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos

# Represents an eye object with an associated image, x position, and y position on the screen
class Eye(FallingObject):
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__(x_pos, y_pos)
        self.img = pygame.image.load('falling_objects/eye.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 100))


# Represents a book object with an associated image, x position, and y position on the screen
class Book():
    def __init__(self, x_pos, y_pos) -> None:
        super().__init__(x_pos, y_pos)
        self.img = pygame.image.load("falling_objects/book.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (160,120))

# Represents the player with an associated image, x position on the screen, and score counter
class Player():
    def __init__(self, x_pos) -> None:
        self.img = pygame.image.load("box.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (200,200))
        self.rect = self.img.get_rect(midbottom = (400, 725))
        self.x_pos = x_pos
        self.score = 0

    def increase_score(self):
        self.score += 1

    def correct_out_of_bounds_x(self):
        if self.rect.left < 0: 
            self.rect.left = 0
        elif self.rect.right > WINDOW_X:
            self.rect.right = WINDOW_X

# Getting background images loaded into variables
background = pygame.image.load('cityscape.png').convert()
floor_background = pygame.Surface((800, 50))
floor_background.fill("#310108")
sky_background = pygame.Surface((800,300))
sky_background.fill("#8a041b")


clock = pygame.time.Clock()

# Setting some constants
player_x_pos = 400
player_y_pos = 530
falling_gravity = 2
player = Player(player_x_pos)

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

    player.correct_out_of_bounds_x()
    screen.blit(player.img, player.rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.move_ip(-5, 0)  # Move left
    if keys[pygame.K_RIGHT]:
        player.rect.move_ip(5, 0) # Move right


    b = Eye(400,30)
    # current objects on the screen
    current_falling_objects = [a, b]

    ''' 
    # Test to see if any object in the list collides:
    if pygame.Rect.collideobjects(player.rect, current_falling_objects):
        pygame.quit()
        exit()
    '''

    # Score text rendering
    score = my_font.render(f"Score: {player.score}", True, "lightgrey", None)
    screen.blit(score, (700, 20))

    pygame.display.flip()
    clock.tick(120)
