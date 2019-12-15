# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import sys

# try imprting rpi libraries, else run desktop mode
try:
    import smbus
    import RPi.GPIO as GPIO
    RPI = True
except:
    RPI = False
    withEncoder = False

# Set up
pygame.init()
    
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

# Define some constants
width = 1920
height = 1080
paddle_width = 15
paddle_height = 150
ball_size = 10
paddle_speed = 8
ball_speed = 20
friction = 10

# Define i2c addresses and RPi GPIOs
ADDRESS1 = 0x04
ADDRESS2 = 0x05
BUTTON1 = 4
BUTTON2 = 14
LEDRED = 15
LEDBLUE = 18

# RPI set up
if RPI:
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
    GPIO.setup(LEDRED, GPIO.OUT)
    GPIO.setup(LEDBLUE, GPIO.OUT)
    GPIO.output(LEDRED, 0)
    GPIO.output(LEDBLUE, 0)

# cool down for buttons
CD1 = False
CD2 = False

# Open a new window
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# create paddles
paddleA = Paddle(RED, paddle_width, paddle_height, height)
paddleA.rect.x = 2*paddle_width
paddleA.rect.y = (height-paddle_height)//2

paddleB = Paddle(BLUE, paddle_width, paddle_height, height)
paddleB.rect.x = width-3*paddle_width
paddleB.rect.y = (height-paddle_height)//2

#create ball
ball = Ball(WHITE,ball_size,ball_size,ball_speed)
ball.rect.x = (width-ball_size)//2
ball.rect.y = (height-ball_size)//2

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the paddles and ball to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball) 

#Initialise player scores
scoreA = 0
scoreB = 0

# Function to move the paddles
def movePaddle():
    if withEncoder:
        try:
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
        except:
            pass

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(paddle_speed)
    if keys[pygame.K_s]:
        paddleA.moveDown(paddle_speed)
    if keys[pygame.K_UP]:
        paddleB.moveUp(paddle_speed)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(paddle_speed)

# Functions to detect if the buttons are pushed
def button1_pushed():
    if RPI:
        global CD1
        if GPIO.input(BUTTON1) == 1 and CD1 == False:
            CD1 = True
            return True
        else:
            return False
    else:
        return False

def button2_pushed():
    if RPI:
        global CD2
        if GPIO.input(BUTTON2) == 1 and CD2 == False:
            CD2 = True
            return True
        else:
            return False
    else:
        return False

# Function to refresh buttons cooldown
def button_refresh():
    if RPI:
        global CD1, CD2
        if GPIO.input(BUTTON1) == 0:
            CD1 = False
        if GPIO.input(BUTTON2) == 0:
            CD2 = False

# Function to reset the game
def reset():
    paddleA.rect.y = (height-paddle_height)//2
    paddleB.rect.y = (height-paddle_height)//2
    ball.rect.x = (width-ball_size)//2
    ball.rect.y = (height-ball_size)//2
    ball.reset()
    pygame.time.delay(1000)
    if withEncoder:
        try:
            I2Cbus.read_byte(ADDRESS1)
            I2Cbus.read_byte(ADDRESS2) #reset encoders
        except:
            reset()

# Function to start a new game
def rematch():
    global scoreA, scoreB
    paddleA.rect.y = (height-paddle_height)//2
    paddleB.rect.y = (height-paddle_height)//2
    ball.rect.x = (width-ball_size)//2
    ball.rect.y = (height-ball_size)//2
    ball.reset()
    scoreA = 0
    scoreB = 0
    if withEncoder:
        try:
            I2Cbus.read_byte(ADDRESS1)
            I2Cbus.read_byte(ADDRESS2) #reset encoders
        except:
            rematch()
    game()

# Function to get text
def get_text(size, string, colour):
    font = pygame.font.Font('assets/kongtext.ttf', size)
    text = font.render(string, 1, colour)
    return text

# Function to check if the game has a winner
def check_win(scoreA, scoreB):
    if scoreA >= 6 and scoreA-scoreB >= 2:
        return 'A'
    elif scoreB >= 6 and scoreB-scoreA >= 2:
        return 'B'
    else:
        return False

# Finishing page
def finish(winner):
    FINISH = True
    clock = pygame.time.Clock()
    global CD1, CD2

    while FINISH:
        # Check quiting 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FINISH = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x:
                        FINISH=False
        if RPI:
            button_refresh()

        # check rematch and escape
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            FINISH = False
            rematch()
        if keys[pygame.K_ESCAPE]:
            FINISH = False
            menu()

        if RPI:
            if button1_pushed():
                FINISH = False
                menu(ready=1)
            if button2_pushed():
                FINISH = False
                menu(ready=2)

        # display text
        if winner == 'A':
            text = get_text(144,"RED WINS!", RED)
            if RPI:
                GPIO.output(LEDRED, 1)       
        elif winner == 'B':
            text = get_text(144,"BLUE WINS!", BLUE)
            if RPI:
                GPIO.output(LEDBLUE, 1)      
        screen.blit(text, ((width-text.get_width())//2,height//3))

        # display instructions
        text = get_text(108, "REMATCH?", WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3))
        if RPI:
            text = get_text(54, "Press button!", WHITE)
        else:
            text = get_text(54, "Press space!", WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3+2*text.get_height()))

        pygame.display.flip()
        clock.tick(60)

# Menu page
def menu(ready=0):
    if RPI:
        GPIO.output(LEDRED, 0)
        GPIO.output(LEDBLUE, 0)
    
    MENU = True
    clock = pygame.time.Clock()
    p1 = True if ready ==1 else False
    p2 = True if ready ==2 else False
    global CD1, CD2

    while MENU:
        # Check quiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MENU = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x:
                        MENU=False
            
        button_refresh()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            MENU = False
            rematch()

        if p1 and p2:
            MENU = False
            pygame.time.delay(1000)
            p1 = False
            p2 = False
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
            ball.bounce(rand=True)

        screen.fill(BLACK)
        
        # reset paddles
        paddleA.rect.y = (height-paddle_height)//2
        paddleB.rect.y = (height-paddle_height)//2

        all_sprites_list.update()
        all_sprites_list.draw(screen)

        # write text
        text = get_text(108, "PONG!", WHITE)
        screen.blit(text, ((width-text.get_width())//2,height//3))
        text = get_text(54, "Press button to start", WHITE)
        screen.blit(text, ((width-text.get_width())//2,height*2//3-text.get_height()))

        if p1:
            font = pygame.font.Font('assets/kongtext.ttf', 54)
            text = font.render("P1 Ready!", 1 , RED)
            screen.blit(text, (width//5,height*3//4))
        if p2:
            font = pygame.font.Font('assets/kongtext.ttf', 54)
            text = font.render("P2 Ready!", 1 , BLUE)
            screen.blit(text, (width*4//5-text.get_width(),height*3//4))
        
        pygame.display.flip()
        clock.tick(60)
        
# The main game loop
def game():
    carryOn = True
    PAUSE = False
    if RPI:
        GPIO.output(LEDRED, 0)
        GPIO.output(LEDBLUE, 0)
    global scoreA, scoreB, CD1, CD2
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
       
    # -------- Main Program Loop -----------
    while carryOn:
        RESET = False
        # --- Main event loop
        # Check quiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x:
                        carryOn=False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            carryOn = False
            menu()

        if PAUSE:
            if button1_pushed() or button2_pushed():
                PAUSE = False
        else:
            if button1_pushed() or button2_pushed():
                PAUSE = True
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
            if withEncoder:
                if pygame.sprite.collide_mask(ball, paddleA):
                    v = I2Cbus.read_byte(ADDRESS1)
                    v = v if v <= 127 else 256-v
                elif pygame.sprite.collide_mask(ball, paddleB):
                    v = I2Cbus.read_byte(ADDRESS2)
                    v = v if v <= 127 else 256-v
                ball.bounce(k=friction, spin=v)

            else:
                if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
                    ball.bounce(rand=True)
        
        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)

        # Draw pause page
        if PAUSE:
            font = pygame.font.Font('assets/kongtext.ttf', 96)
            text = font.render("PAUSE", 1, WHITE)
            screen.blit(text, ((width-text.get_width())//2,height//3))
            font = pygame.font.Font('assets/kongtext.ttf', 48)
            text = font.render("press any button to continue", 1, WHITE)
            screen.blit(text, ((width-text.get_width())//2,height*2//3))

        # Draw the net
        pygame.draw.line(screen, WHITE, [width//2, 0], [width//2, height], 5)
        
        # Draw all the sprites in one go
        all_sprites_list.draw(screen) 

        # Display scores
        text = get_text(45, str(scoreA), WHITE)
        screen.blit(text, (width//3,height//50))
        text = get_text(45, str(scoreB), WHITE)
        screen.blit(text, (2*width//3-text.get_width(),height//50))

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
        button_refresh()
        clock.tick(60)
    
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()
    if RPI:
        GPIO.cleanup()

if __name__ == '__main__':
    menu()
