import pygame
from random import randint

BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):
    # This class represents the ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, speed):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color, width ,height and speed of the ball.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.speed = speed
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [self.speed,randint(-self.speed,self.speed)]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    # update ball position    
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    # when ball collides with paddles
    def bounce(self, k=0, spin=0, rand=False):
        # k:friction, spin:paddle velocity, rand:random mode
        self.velocity[0] = -self.velocity[0]
        if rand:
            self.velocity[1] = randint(-self.speed,self.speed)
        else:
            self.velocity[1] = -self.velocity[1] + k * spin

    # randomise ball speed when resetting
    def reset(self):
        self.velocity[1] = randint(-self.speed,self.speed)
