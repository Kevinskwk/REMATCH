# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import sys
import serial

try:
    encoder = serial.Serial('/dev/ttyACM0',9600)
    encoder.flushInput()
    withEncoder = True
except:
    withEncoder = False

pygame.init()
    
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

# Define some constant
width = 1200
height = 800
paddle_width = 10
paddle_height = 100
ball_size = 10
paddle_speed = 10
font_size = 45

# Open a new window
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(RED, paddle_width, paddle_height, height)
paddleA.rect.x = 2*paddle_width
paddleA.rect.y = (height-paddle_height)/2

paddleB = Paddle(BLUE, paddle_width, paddle_height, height)
paddleB.rect.x = width-3*paddle_width
paddleB.rect.y = (height-paddle_height)/2

ball = Ball(WHITE,ball_size,ball_size)
ball.rect.x = (width-ball_size)/2
ball.rect.y = (height-ball_size)/2

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

#Initialise player scores
scoreA = 0
scoreB = 0

def reset():
    paddleA.rect.y = (height-paddle_height)/2
    paddleB.rect.y = (height-paddle_height)/2
    ball.rect.x = (width-ball_size)/2
    ball.rect.y = (height-ball_size)/2
    pygame.time.delay(1000)

def rematch():
    global scoreA, scoreB
    paddleA.rect.y = (height-paddle_height)/2
    paddleB.rect.y = (height-paddle_height)/2
    ball.rect.x = (width-ball_size)/2
    ball.rect.y = (height-ball_size)/2
    scoreA = 0
    scoreB = 0

def display_score(scoreA, scoreB):
    #Display scores:
    font = pygame.font.Font('assets/kongtext.ttf', font_size)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (width/3,15))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (2*width/3-font_size/2,15))

def main():
    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True

    global scoreA, scoreB
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
            
    # -------- Main Program Loop -----------
    while carryOn:
        RESET = False
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                        carryOn=False

        #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
        if withEncoder:
            if encoder.inWaiting() > 0:
                cmd = ord(encoder.read(1))
                if cmd == 1:
                    paddleB.moveUp(paddle_speed)
                if cmd == 2:
                    paddleB.moveDown(paddle_speed)
                if cmd == 3:
                    paddleA.moveUp(paddle_speed)
                if cmd == 4:
                    paddleA.moveDown(paddle_speed)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddleA.moveUp(paddle_speed)
        if keys[pygame.K_s]:
            paddleA.moveDown(paddle_speed)
        if keys[pygame.K_UP]:
            paddleB.moveUp(paddle_speed)
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(paddle_speed)

        # --- Game logic should go here
        all_sprites_list.update()
        
        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=width-ball_size:
            ball.rect.x = width-ball_size
            scoreA+=1
            ball.velocity[0] = -ball.velocity[0]
            RESET = True

        if ball.rect.x<=0:
            ball.rect.x = 0
            scoreB+=1
            ball.velocity[0] = -ball.velocity[0]
            RESET = True

        if ball.rect.y>height-ball_size:
            ball.rect.y = height-ball_size
            ball.velocity[1] = -ball.velocity[1]
            
        if ball.rect.y<0:
            ball.rect.y = 0
            ball.velocity[1] = -ball.velocity[1]     
    
        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
            ball.bounce()
        
        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(screen, WHITE, [width/2, 0], [width/2, height], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen) 

        display_score(scoreA,scoreB)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        if RESET:
            reset()

        # --- Limit to 60 frames per second
        clock.tick(60)
    
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()

if __name__ == '__main__':
    main()