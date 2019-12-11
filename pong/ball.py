import pygame
from random import randint

BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, speed):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.speed = speed
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [randint(self.speed,3*self.speed//2),randint(-self.speed,self.speed)]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-self.speed,self.speed)

    def reset(self):
        self.velocity[1] = randint(-self.speed,self.speed)
