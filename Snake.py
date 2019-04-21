"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""
from enum import Enum

import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

class Direction():
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

UP = Direction(0,-1)
RIGHT = Direction(1,0)
DOWN = Direction(0,1)
LEFT = Direction(-1,0)

class Part():
    SIZE = 30

    def __init__(self):
        self.direction = RIGHT
        self.nextDirection = None
        self.progress = 0
        self.position = [0,0]

    def update(self, delta):
        self.progress += delta * 15
        
        if self.progress >= 1:
            while self.progress >= 1:
                self.position[0] += self.direction.dx
                self.position[1] += self.direction.dy
                self.progress -= 1

            if self.nextDirection is not None:
                self.direction = self.nextDirection
                self.nextDirection = None


    def render(self, screen):
        px = self.position[0] + self.progress * self.direction.dx
        py = self.position[1] + self.progress * self.direction.dy

        pygame.draw.ellipse(screen, RED, [px* Part.SIZE, py * Part.SIZE, Part.SIZE, Part.SIZE])

pygame.init()

# Set the width and height of the screen [width, height]
size = (600, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake")

# Loop until the user clicks the close button.
done = False
gameOver = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

parts = []
head = Part()
head.position = [3,0]
parts.append(head)

def addPart():
    last = parts[len(parts)-1]
    part = Part()
    
    part.position[0] = last.position[0] - 1
    part.position[1] = last.position[1] 
    parts.append( part )

for i in range(3):
    addPart()

foodX = random.randint(0, int(600/Part.SIZE) -1)
foodY = random.randint(0, int(600/Part.SIZE) -1)
food = [foodX, foodY]

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and not gameOver:
            if event.key == pygame.K_RIGHT:
                if head.direction is not LEFT:
                    head.nextDirection = RIGHT
            elif event.key == pygame. K_LEFT:
                if head.direction is not RIGHT:
                    head.nextDirection = LEFT
            elif event.key == pygame.K_UP:
                if head.direction is not DOWN:
                    head.nextDirection = UP
            elif event.key == pygame. K_DOWN:
                if head.direction is not UP:
                    head.nextDirection = DOWN
                
    # --- Game logic should go here
    for i in range( 1, len(parts) ):
        parts[ i ].nextDirection = parts[ i - 1 ].direction


    if head.position[0] == food[0] and head.position[1] == food[1]:
        addPart()
        foodX = random.randint(0, int(600 / Part.SIZE) -1)
        foodY = random.randint(0, int(600 / Part.SIZE) -1)
        food = [foodX, foodY]

    for part in parts:
        width = int(600/Part.SIZE) - 1
        height = int(600/Part.SIZE) - 1

        part.position[0] %= width
        part.position[1] %= height

    for i in range (1, len(parts)):
        if head.position[0] == parts[i].position[0] and head.position[1] == parts[i].position[1]:
            gameOver = True


    for part in parts:
        part.update(1.0/60)
    
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)

    # --- Drawing code should go here
    for part in parts:
        part.render(screen)
    pygame.draw.ellipse(screen,BLUE,[food[0] * Part.SIZE, food[1] * Part.SIZE, Part.SIZE, Part.SIZE])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
    
# Close the window and quit.
pygame.quit()