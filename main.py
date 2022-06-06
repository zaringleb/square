# Simple pygame program

from dataclasses import dataclass
from re import S
import enum

# Import and initialize the pygame library
from turtle import distance
import pygame
from math import pi


from pygame.locals import (
    K_ESCAPE,
    K_t,
    KEYDOWN,
    QUIT,
)


pygame.init()

BLACK = (0, 0, 0)
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200
FRAME_RATE = 30

 
class Smile(enum.Enum):
    absent = 0
    closed = 1
    open = 2
    sad = 3
    smile = 4

@dataclass
class Point:
    x: float
    y: float


class Eye:
    def __init__(self, left=True) -> None:
        self.eye_width = 1 / 6
        self.eye_height = 1 / 8
        self.distance_from_center_to_eye = [1 / 4 if left else - 1 / 4, 1 / 6]
        self.is_closed = False

    
    def draw(self, screen, center, size):
        eye_width = size * self.eye_width
        eye_height = 1 if self.is_closed else size * self.eye_height
        distance_from_center_to_eye = [
            size * self.distance_from_center_to_eye[0],
            size * self.distance_from_center_to_eye[1]
            ]

        eye = (
            center.x - distance_from_center_to_eye[0] - eye_width // 2,
            center.y - distance_from_center_to_eye[1] - eye_height // 2,
            eye_width, eye_height
            )
        pygame.draw.ellipse(screen, BLACK, eye)


class Mouth:
    def __init__(self) -> None:
        self.width = 1 / 3
        self.height = 1 / 8
        self.distance_from_center = [0, -1 / 6]
        self.smile = Smile.absent

    
    def draw(self, screen, center, size):

        xy = [center.x, center.y + 5]
        #pygame.draw.ellipse(screen, BLACK, rect, width=3)
        if self.smile == Smile.smile:
            pygame.draw.circle(screen, BLACK, [center.x, center.y + size / 16], size / 5, 0, False, False, True, True)
        elif self.smile == Smile.open:
            pygame.draw.circle(screen, BLACK, [center.x, center.y + size / 8], size / 7, 0)
        elif self.smile == Smile.sad:
            pygame.draw.circle(screen, BLACK, [center.x, center.y + size / 4], size / 5, 3, True, True, False, False)
        elif self.smile == Smile.closed:
            pygame.draw.line(screen, BLACK, [center.x - size / 7, center.y + size / 8], [center.x + size / 7, center.y + + size / 8], 3)
        else:
            pass


class Square:
    def __init__(self, size: float) -> None:
        self.size = size
        self.center = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT - size // 2 - 10)
        self.left_eye = Eye(left=True)
        self.right_eye = Eye(left=False)
        self.mouth = Mouth()

    def draw(self, screen):
        body = pygame.Rect(self.center.x - self.size // 2, self.center.y - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, (255, 100, 255), body, width=0, border_radius= self.size // 5)
        pygame.draw.rect(screen, BLACK, body, width=3, border_radius= self.size // 5)
        self.left_eye.draw(screen, self.center, self.size)
        self.right_eye.draw(screen, self.center, self.size)
        self.mouth.draw(screen, self.center, self.size)


def blink(time):
    count = time

    def action(square):
        nonlocal count
        if count == time:
            is_first_time = False
            square.left_eye.is_closed = True
            square.right_eye.is_closed = True
        if count == 0:
            square.left_eye.is_closed = False
            square.right_eye.is_closed = False
            return False
        count -= 1
    
    return action


def jump(v, g=0.5):
    h = 0
    def action(square):
        nonlocal h, v
        v -= g
        h += v
        square.center.y -= v
        if h <= 0:
            square.center.y -= h
            return False
    return action


def dance(step, dt):
    count = int(dt * FRAME_RATE)
    step_size = step / count
    direction = 1

    def action(square):
        nonlocal count, direction
        square.center.x += direction * step_size
        count -= 1
        if count == 0:
            count = int(dt * FRAME_RATE)
            direction = -direction
    return action


def speak():
    count = 0
    dt = 3
    talk = []
    for o in (1, 1, 0, 1, 1, 1, 0):
        talk.extend(([1 for _ in range(dt)] if o else []) + [0 for _ in range(dt)])
    talk = talk * 2

    def action(square):
        nonlocal count
        if talk[count]:
            square.mouth.smile = Smile.closed
        else:
            square.mouth.smile = Smile.open
        count += 1
        if count == len(talk):
            square.mouth.smile = Smile.smile
            return False

    
    return action



screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

square = Square(80)

h = SCREEN_HEIGHT - square.center.y - square.size // 2
clock = pygame.time.Clock()

#actions = {'jump': jump(6)}
actions = {} #{'dance': dance(30, 1.0)}

start_ticks=None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                actions = {}
            elif event.key == K_t:
                actions = {'dance': dance(30, 1.0)}
                start_ticks=pygame.time.get_ticks() #starter tick

    if start_ticks is not None:
        if (pygame.time.get_ticks()-start_ticks)/1000 > 60 * 20: #calculate how many seconds
            start_ticks = None
            actions = {'jump': jump(6)}
    
    screen.fill((255, 255, 255))
    
    new_actions = {}
    for name, action in actions.items():
        if action(square) != False:
            new_actions[name] = action
        else:
            if name == 'jump':
                new_actions['jump'] = jump(6)
                new_actions['blink'] = blink(4)

    actions = new_actions

    square.draw(screen)


    # Flip the display
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
