import pygame
BLACK = (0,0,0)
 
class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, screen_height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color, width, height of the paddle and the height of the screen
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.range = screen_height-height
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
		# Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
	    # Check that you are not going too far (off the screen)
        if self.rect.y > self.range:
          self.rect.y = self.range
