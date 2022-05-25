# Simple pygame program

# Import and initialize the pygame library
from turtle import distance
import pygame
from math import pi
pygame.init()

BLACK = (0, 0, 0)
L = 80
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Run until the user asks to quit
running = True
center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - L // 2 + 1]


h = SCREEN_HEIGHT - center[1] - L // 2
c = 0
d = 1
v = 6
clock = pygame.time.Clock()
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if c == 0:
        d = -1
    if c == -20:
        d = 1

    #body.move_ip(d, 0)
    c += d
    
    a = -0.5
    v = v + a
    if h <= 0:
        v = 6
    h += v
    center[1] = SCREEN_HEIGHT - L // 2 + 1 - h
    # Fill the background with white
    screen.fill((255, 255, 255))

    body = pygame.Rect(center[0] - L // 2, center[1] - L // 2, L, L)
    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (100, 100), 30)
    pygame.draw.rect(screen, BLACK, body, width=3, border_radius=L // 5)

    eye_width = L // 6
    eye_height = L // 8 if h >= 10 else 1
    distance_from_center_to_eye = [L // 4, L // 6]

    # left
    eye = (
        center[0] - distance_from_center_to_eye[0] - eye_width // 2,
        center[1] - distance_from_center_to_eye[1] - eye_height // 2,
        eye_width, eye_height
        )
    
    #pygame.draw.rect(screen, BLACK, eye, width=1)
    pygame.draw.ellipse(screen, BLACK, eye)

    # right
    eye = (
        center[0] + distance_from_center_to_eye[0] - eye_width // 2,
        center[1] - distance_from_center_to_eye[1] - eye_height // 2,
        eye_width, eye_height
        )
    pygame.draw.ellipse(screen, BLACK, eye)
    #pygame.draw.arc(screen, BLACK, eye, 0, pi)



    # Flip the display
    pygame.display.flip()
    clock.tick(30)

# Done! Time to quit.
pygame.quit()
