from enum import Enum

import pygame
import random

class Direction():
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class Part():
    SIZE = 30

    def __init__(self,direction):
        self.direction = direction
        self.nextDirection = None
        self.position = (0,0)

    def update(self):
        self.position = (self.position[0] + self.direction.dx, self.position[1] + self.direction.dy)
        
        if self.nextDirection is not None:
            self.direction = self.nextDirection
            self.nextDirection = None


    def render(self, screen, progress):
        px = self.position[0] + progress * self.direction.dx
        py = self.position[1] + progress * self.direction.dy

        pygame.draw.ellipse(screen, RED, [px* Part.SIZE, py * Part.SIZE, Part.SIZE, Part.SIZE])

#Directions
UP = Direction(0,-1)
RIGHT = Direction(1,0)
DOWN = Direction(0,1)
LEFT = Direction(-1,0)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0,0,255)

# Screen-related variables
size = (600, 600)
pwidth = size[0]
pheight = size[1]
screen = pygame.display.set_mode(size)

#pygame
pygame.display.set_caption("Snake")
pygame.init()

# Game-logic variables
done = False
gameOver = False
progress = 0
clock = pygame.time.Clock()

# Game-logic (snake) variables
parts = []
head = Part(RIGHT)
head.position = (0,0)
parts.append(head)

# Game-logic (food) variables
foodX = random.randint(0, int(pwidth/Part.SIZE) - 1)
foodY = random.randint(0, int(pheight/Part.SIZE) - 1)
food = (foodX, foodY)

#Rendering variables
font = pygame.font.SysFont('Calibri', 30)

# Global method
def addPart():
    last = parts[-1]
    lastDirection = last.direction
    part = Part(lastDirection)
    
    part.position = (last.position[0] - lastDirection.dx, last.position[1] - lastDirection.dy )
    parts.append( part )

# Game loop
while not done:
    # Event loop
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
    
    if not gameOver:
        # Main logic
        for i in range( 1, len(parts) ):
            parts[ i ].nextDirection = parts[ i - 1 ].direction


        # Collision and bounds check
        if head.position == food:
            addPart()
            foodX = random.randint(0, int(pwidth / Part.SIZE) - 1)
            foodY = random.randint(0, int(pheight / Part.SIZE) - 1)
            food = (foodX, foodY)

        for part in parts:
            width = int(pwidth/Part.SIZE)
            height = int(pheight/Part.SIZE)

            part.position = (part.position[0] % width, part.position[1] % height)
        
        for i in range (1, len(parts)):
            if head.position == parts[i].position:
                gameOver = True
            
        # Updating part positions
        delta = 1.0 / 60
        progress += delta * 15
        
        if progress >= 1:
            while progress >= 1:
                progress -= 1
            
                for part in parts:
                    part.update()
    
    # Rendering
    screen.fill(WHITE)

    # Main render part    
    for part in parts:
        part.render(screen, progress)
    pygame.draw.ellipse(screen,BLUE,[food[0] * Part.SIZE, food[1] * Part.SIZE, Part.SIZE, Part.SIZE])
    
    if(gameOver):
        alphaSurface = pygame.Surface((pwidth,pheight), pygame.SRCALPHA)
        alphaSurface.fill((0,0,0,150))                         
        screen.blit(alphaSurface, (0,0))
        textSurface = font.render('Verloren...', False, WHITE)
        screen.blit(textSurface, (pwidth / 2 - textSurface.get_width() / 2, pheight / 2 - textSurface.get_height() / 2))
    
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()