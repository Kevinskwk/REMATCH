import pygame
from sqlite_helper import create_connection, sort_highest

# Initiate sqlite database
conn = create_connection('database.sqlite')

# Initiate leaderboard
pygame.init()

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Open a new window
size = (800, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("LeaderBoard")

carryOn = True
clock = pygame.time.Clock()


while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False

    data = sort_highest(conn)
    data = data[0:10] if len(data)>10 else data
    

    screen.fill(BLACK)

    title_font = pygame.font.Font(None, 85)
    single = title_font.render("Single Time", 1, WHITE)
    screen.blit(single,(250,30))

    font = pygame.font.Font(None, 74)
    title_rank = font.render("Rank", 1, WHITE)
    screen.blit(title_rank, (50,100))
    title_name = font.render("Name", 1, WHITE)
    screen.blit(title_name, (300,100))
    title_score = font.render("Score", 1, WHITE)
    screen.blit(title_score, (600,100))

    for i in range(len(data)):
        rank = font.render(str(i+1), 1, WHITE)
        screen.blit(rank,(100,170+70*i))
        name = font.render(str(data[i]["First_name"]), 1, WHITE)
        screen.blit(name,(300,170+70*i))
        score = font.render(str(data[i]["Highest"]), 1, WHITE)
        screen.blit(score,(650,170+70*i))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()