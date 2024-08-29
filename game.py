from typing import Any
import pygame
from sys import exit
import random
import threading
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

pygame.init()

# Set up of game window
WINDOW_X = 800
WINDOW_Y = 700
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('Escaping Big Brother')
programIcon = pygame.image.load('1984-bbimg.jpeg').convert()
pygame.display.set_icon(programIcon)
my_font = pygame.font.SysFont('Arial', 15)
end_font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

# Represents a falling object (object the player either avoids or tries to obtain)
class FallingObject():
    def __init__(self, x_pos, y_pos, speed) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed


# Represents an eye object with an associated image, x position, and y position on the screen
class Eye(FallingObject):
    def __init__(self, x_pos, y_pos, speed) -> None:
        super().__init__(x_pos, y_pos, speed)
        self.img = pygame.image.load('falling_objects/eye.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (65, 65))
        self.rect = self.img.get_rect(midbottom = (x_pos, y_pos))

    def move(self):
        self.rect.move_ip(0, + self.speed) # move by object's defined speed


# Represents a book object with an associated image, x position, and y position on the screen
class Book(FallingObject):
    def __init__(self, x_pos, y_pos, speed) -> None:
        super().__init__(x_pos, y_pos, speed)
        self.img = pygame.image.load("falling_objects/book.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (90,65))
        self.rect = self.img.get_rect(midbottom = (x_pos, y_pos))
    
    def move(self):
        self.rect.move_ip(0, + self.speed) # move by object's defined speed


# Represents the player with an associated image, x position on the screen, and score counter
class Player():
    def __init__(self, x_pos) -> None:
        self.img = pygame.image.load("box.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (100,100))
        self.rect = self.img.get_rect(midbottom = (400, 700))
        self.x_pos = x_pos
        self.score = 0

    def increase_score(self):
        self.score += 1

    def correct_out_of_bounds_x(self):
        if self.rect.left < 0: 
            self.rect.left = 0
        elif self.rect.right > WINDOW_X:
            self.rect.right = WINDOW_X

    def collision(self, falling_objects: list):
        # Test to see if any object in the list collides:
        if pygame.Rect.collideobjects(self.rect, falling_objects):
            return True

# Getting background images loaded into variables
background = pygame.image.load('cityscape.png').convert()
floor_background = pygame.Surface((800, 50))
floor_background.fill("#310108")
sky_background = pygame.Surface((800,300))
sky_background.fill("#8a041b")


# Setting some constants
player_x_pos = 400
player_y_pos = 530
player = Player(player_x_pos)
game_active = True

# Instantiating falling objects with x coord & speed and placing them in a list
falling_objects = []
eyes_list = []
speeds = [1,2,3]
for i in range(3):
    e = Eye(random.randrange(0, WINDOW_X), 0, speeds[i])
    falling_objects.append(e), eyes_list.append(e)
b = Book(random.randrange(0, WINDOW_X), 0, 2)
falling_objects.append(b)


# Initializing x_cur and x_prev !!! TO-DO
x_cur = None
x_prev = None
# Setting a lock that will be changing the value of x_prev in both threads
x_lock = threading.Lock()


# Setting up face detection thread
def face_detection():
    global x_cur, x_prev

    model_path = 'blaze_face_short_range.tflite'

    BaseOptions = mp.tasks.BaseOptions
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    FaceDetectorResult = mp.tasks.vision.FaceDetectorResult
    VisionRunningMode = mp.tasks.vision.RunningMode

    def print_result(result: FaceDetectorResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
        global x_cur, x_prev
        if result.detections:
            x_cur = get_x_value(result)             # This continuously updates the player's current head position
            x_lock.acquire()                                
            if x_prev is None:                      # This initializes x_prev at the start with player's original head position
                x_prev = get_x_value(result)
            x_lock.release()
        else:
            return "No face detected"

    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

    def get_x_value(detection_result):
        for detection in detection_result.detections:
            x = detection.bounding_box.origin_x + (detection.bounding_box.width/2)
            return x

    with FaceDetector.create_from_options(options) as detector:
        cam = cv2.VideoCapture(1)  # Use the default webcam
        
        while cam.isOpened():
            success, img = cam.read()
            if not success:
                print("Failed to read from camera")
                break

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
            
            # Get the current time in milliseconds
            frame_timestamp_ms = int(time.time() * 1000)
            
            # Perform face detection asynchronously
            detector.detect_async(mp_image, frame_timestamp_ms)

        cam.release()
        cv2.destroyAllWindows()

# stop this motion detection thread after all other code is completed
threading.Thread(target = face_detection, daemon=True).start()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        # Setting background images on screen
        screen.blit(sky_background, (0,0))
        screen.blit(background, (0,300))
        screen.blit(floor_background, (0, 650))

        # Simulate objects falling from top of screen
        for obj in falling_objects:
            if obj.rect.top > WINDOW_Y:
                obj.rect.midbottom = (random.randrange(0, WINDOW_X), 0)
            screen.blit(obj.img, obj.rect)
            obj.move()

        # Check if player is out of bounds and place it within screen bounds
        player.correct_out_of_bounds_x()
        screen.blit(player.img, player.rect)

        # Handling player movements with a keyboard version
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     player.rect.move_ip(-5, 0)  # Move left
        # if keys[pygame.K_RIGHT]:
        #     player.rect.move_ip(5, 0)   # Move right
        
        # If x-coordinates moved > 20 coordinates, move player 20 units left/right on screen
        # Then set x_current = x_prev if above conditions are true
        if x_cur is not None and x_prev is not None and abs(x_prev - x_cur) >= 20:
            if x_cur > x_prev: # move left
                player.rect.move_ip(-20, 0)
                x_prev = x_cur
            else:  # move right
                player.rect.move_ip(20, 0) 
                x_prev = x_cur
        

        # Score text rendering
        score = my_font.render(f"Score: {player.score}", True, "lightgrey", None)
        screen.blit(score, (700, 20))

        if player.collision(eyes_list):
            game_active = False                                         # If collision w/ eye, end game
        elif pygame.Rect.colliderect(player.rect, b.rect):
            player.increase_score()                                     # If collision w/ book, increase score
            b.rect.midbottom = (random.randrange(0, WINDOW_X), 0)       # Send book to top of screen (disappear)
    else:
        screen.fill("#160121")
        display1 = end_font.render('You lost!', True, "white", None)
        display2 = end_font.render(f'You Scored: {player.score} points', True, "white", None)
        screen.blit(display1, (350, 200))
        screen.blit(display2, (275, 350))

                    
    pygame.display.flip()
    clock.tick(60)



    