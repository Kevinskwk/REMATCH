# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import sys
import smbus
import RPi.GPIO as GPIO

# Set up
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
ball_speed = 10
font_size = 45
ADDRESS1 = 0x04
ADDRESS2 = 0x05
BUTTON1 = 4
BUTTON2 = 14

try:
    I2Cbus = smbus.SMBus(1)
    I2Cbus.read_byte(ADDRESS1)
    I2Cbus.read_byte(ADDRESS2)
    withEncoder = True
except:
    withEncoder = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
CD1 = False
CD2 = False

# Open a new window
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(RED, paddle_width, paddle_height, height)
paddleA.rect.x = 2*paddle_width
paddleA.rect.y = (height-paddle_height)//2

paddleB = Paddle(BLUE, paddle_width, paddle_height, height)
paddleB.rect.x = width-3*paddle_width
paddleB.rect.y = (height-paddle_height)//2

ball = Ball(WHITE,ball_size,ball_size,ball_speed)
ball.rect.x = (width-ball_size)//2
ball.rect.y = (height-ball_size)//2

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball) 

#Initialise player scores
scoreA = 0
scoreB = 10

def movePaddle():
    if withEncoder:
        cmd1 = I2Cbus.read_byte(ADDRESS1)
        cmd2 = I2Cbus.read_byte(ADDRESS2)
        if cmd1 <= 127:
            paddleA.moveUp(cmd1*paddle_speed)
        if cmd1 >= 128:
            paddleA.moveDown((256-cmd1)*paddle_speed)
        if cmd2 <= 127:
            paddleB.moveUp(cmd2*paddle_speed)
        if cmd2 >= 128:
            paddleB.moveDown((256-cmd2)*paddle_speed)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(paddle_speed)
    if keys[pygame.K_s]:
        paddleA.moveDown(paddle_speed)
    if keys[pygame.K_UP]:
        paddleB.moveUp(paddle_speed)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(paddle_speed)

def button1_pushed():
    global CD1
    if GPIO.input(BUTTON1) == 1 and CD1 == False:
        CD1 = True
        return True
    else:
        return False

def button2_pushed():
    global CD2
    if GPIO.input(BUTTON2) == 1 and CD2 == False:
        CD2 = True
        return True
    else:
        return False

def button_refresh():
    global CD1, CD2
    if GPIO.input(BUTTON1) == 0:
        CD1 = False
    if GPIO.input(BUTTON2) == 0:
        CD2 = False

def reset():
    paddleA.rect.y = (height-paddle_height)//2
    paddleB.rect.y = (height-paddle_height)//2
    ball.rect.x = (width-ball_size)//2
    ball.rect.y = (height-ball_size)//2
    ball.reset()
    pygame.time.delay(1000)
    I2Cbus.read_byte(ADDRESS1)
    I2Cbus.read_byte(ADDRESS2) #reset encoders

def rematch():
    global scoreA, scoreB
    paddleA.rect.y = (height-paddle_height)//2
    paddleB.rect.y = (height-paddle_height)//2
    ball.rect.x = (width-ball_size)//2
    ball.rect.y = (height-ball_size)//2
    ball.reset()
    scoreA = 0
    scoreB = 0
    I2Cbus.read_byte(ADDRESS1)
    I2Cbus.read_byte(ADDRESS2) #reset encoders
    game()

def display_score(scoreA, scoreB):
    #Display scores:
    font = pygame.font.Font('assets/kongtext.ttf', font_size)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (width//3,height//50))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (2*width//3-text.get_width(),height//50))

def check_win(scoreA, scoreB):
    if scoreA >= 6 and scoreA-scoreB >= 2:
        return 'A'
    elif scoreB >= 6 and scoreB-scoreA >= 2:
        return 'B'
    else:
        return False

def finish(winner):
    FINISH = True
    clock = pygame.time.Clock()

    while FINISH:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                FINISH = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                        FINISH=False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            FINISH = False
            rematch()
        if keys[pygame.K_ESCAPE]:
            FINISH = False
            menu()

        if button1_pushed():
            FINISH = False
            menu(ready=1)
        if button2_pushed():
            FINISH = False
            menu(ready=2)

        screen.fill(BLACK)

        # display text
        if winner == 'A':
            font = pygame.font.Font('assets/kongtext.ttf', 144)
            text = font.render("RED WIN!", 1, RED)
            screen.blit(text, ((width-text.get_width())//2,height//3))
        elif winner == 'B':
            font = pygame.font.Font('assets/kongtext.ttf', 144)
            text = font.render("BLUE WIN!", 1, BLUE)
            screen.blit(text, ((width-text.get_width())//2,height//3))

        # display instructions
        font = pygame.font.Font('assets/kongtext.ttf', 108)
        text = font.render("REMATCH?", 1, WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3))
        font = pygame.font.Font('assets/kongtext.ttf', 54)
        text = font.render("Press button!", 1, WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3+2*text.get_height()))


        pygame.display.flip()
        button_refresh
        clock.tick(60)

def menu(ready=0):
    MENU = True
    clock = pygame.time.Clock()
    p1 = True if ready ==1 else False
    p2 = True if ready ==2 else False

    while MENU:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                MENU = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                        MENU=False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            MENU = False
            rematch()

        if p1 and p2:
            MENU = False
            pygame.time.delay(1000)
            rematch()

        if button1_pushed():
            if p1 == False:
                p1 = True
            else:
                p1 = False
        if button2_pushed():
            if p2 == False:
                p2 = True
            else:
                p2 = False

        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=width-ball_size:
            ball.rect.x = width-ball_size
            ball.velocity[0] = -ball.velocity[0]

        if ball.rect.x<=0:
            ball.rect.x = 0
            ball.velocity[0] = -ball.velocity[0]

        if ball.rect.y>height-ball_size:
            ball.rect.y = height-ball_size
            ball.velocity[1] = -ball.velocity[1]
            
        if ball.rect.y<0:
            ball.rect.y = 0
            ball.velocity[1] = -ball.velocity[1]     
    
        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
            ball.bounce()

        screen.fill(BLACK)
        
        # reset paddles
        paddleA.rect.y = (height-paddle_height)//2
        paddleB.rect.y = (height-paddle_height)//2

        all_sprites_list.update()
        all_sprites_list.draw(screen)

        # write text
        font = pygame.font.Font('assets/kongtext.ttf', 144)
        text = font.render("PONG!", 1, WHITE)
        screen.blit(text, ((width-text.get_width())//2,height//3))
        font = pygame.font.Font('assets/kongtext.ttf', 72)
        text = font.render("Press button to start", 1, WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3))

        if p1:
            font = pygame.font.Font('assets/kongtext.ttf', 54)
            text = font.render("P1 Ready!", 1 , RED)
            screen.blit(text, (width//5,height*3//4))
        if p2:
            font = pygame.font.Font('assets/kongtext.ttf', 54)
            text = font.render("P2 Ready!", 1 , BLUE)
            screen.blit(text, (width*4//5-text.get_width()//2,height*3//4))
        
        pygame.display.flip()
        button_refresh()
        clock.tick(60)
        

def game():
    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carryOn = True
    PAUSE = False

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
    
        if button1_pushed() or button2_pushed():
            PAUSE = True
        
        if PAUSE:
            if button1_pushed() or button2_pushed():
                PAUSE = False
        
        else:
            movePaddle()
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

        if PAUSE:
            font = pygame.font.Font('assets/kongtext.ttf', 144)
            text = font.render("PAUSE", 1, WHITE)
            screen.blit(text, ((width-text.get_width())//2,height//3))
            font = pygame.font.Font('assets/kongtext.ttf', 72)
            text = font.render("press any button to continue", 1, WHITE)
            screen.blit(text, ((width-text.get_width())//2,height*2//3))

        #Draw the net
        pygame.draw.line(screen, WHITE, [width//2, 0], [width//2, height], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen) 

        display_score(scoreA,scoreB)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        winner = check_win(scoreA,scoreB)
        if winner:
            carryOn = False
            RESET = True
            finish(winner)

        if RESET:
            reset()

        # --- Limit to 60 frames per second
        button_refresh
        clock.tick(60)
    
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()

if __name__ == '__main__':
    menu()