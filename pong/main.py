# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import sys
import serial

encoder = serial.Serial('/dev/ttyACM0',9600)
encoder.flushInput()

pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (1280, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 300
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 1260
paddleB.rect.y = 300
 
ball = Ball(WHITE,10,10)
ball.rect.x = 635
ball.rect.y = 345
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0
#prev = 0
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False

    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
    if encoder.inWaiting() > 0:
        cmd = ord(encoder.read(1))
        if cmd == 1:
            paddleB.moveUp(15)
        if cmd == 2:
            paddleB.moveDown(15)
        if cmd == 3:
            paddleA.moveUp(15)
        if cmd == 4:
            paddleA.moveDown(15)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(15)
    if keys[pygame.K_s]:
        paddleA.moveDown(15)
    if keys[pygame.K_UP]:
        paddleA.moveUp(15)
    if keys[pygame.K_DOWN]:
        paddleA.moveDown(15)

    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=1270:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>690:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [639, 0], [639, 700], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (540,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (710,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
