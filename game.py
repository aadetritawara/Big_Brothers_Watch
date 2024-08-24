import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,750))
pygame.display.set_caption('Escaping Big Brother')

programIcon = pygame.image.load('Facial_Detection_Falling_Object_Game/1984-bbimg.jpeg').convert()
pygame.display.set_icon(programIcon)

eye = pygame.image.load('Facial_Detection_Falling_Object_Game/falling_objects/eye.png').convert_alpha()
eye = pygame.transform.scale(eye, (100, 100))

book = pygame.image.load("Facial_Detection_Falling_Object_Game/falling_objects/book.png").convert_alpha()
book = pygame.transform.scale(book, (160,120))

player = pygame.image.load("Facial_Detection_Falling_Object_Game/box.png").convert_alpha()
player = pygame.transform.scale(player, (200,200))

background = pygame.image.load('Facial_Detection_Falling_Object_Game/cityscape.png').convert()
floor_background = pygame.Surface((800, 50))
floor_background.fill("#310108")
sky_background = pygame.Surface((800,300))
sky_background.fill("#8a041b")


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_background, (0,0))
    screen.blit(background, (0,300))
    screen.blit(floor_background, (0, 700))

    screen.blit(eye, (10,10))
    screen.blit(book, (150,50))

    screen.blit(player, (400,560))
    pygame.display.update()
    clock.tick(60)
