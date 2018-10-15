import sys, pygame
pygame.init()

size = width, height = 1500, 1000
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
food = pygame.image.load("food.png")
foodrect = food.get_rect()
obstacle = pygame.image.load("big_obstacle.png")

playerspeed = [0, 0]
foodrect.topright = (width, 0)
foodspeed = [-1, -1]
obstacles = [
    obstacle.get_rect(),
    obstacle.get_rect(),
    obstacle.get_rect(),
    obstacle.get_rect(),
    obstacle.get_rect()
]
obstacles[0].center = (width/2, height/2)
obstacles[1].center = (width/4, height/4)
obstacles[2].center = (3*width/4, 3*height/4)
obstacles[3].center = (3*width/4, height/4)
obstacles[4].center = (width/4, 3*height/4)
score = 0

print("Game started!")

# setspeed sets speed based on arrow keys pressed
def setspeed(speed):
    if pygame.key.get_pressed()[pygame.K_UP] and ballrect.top > 0:
        speed[1] = -2
    if pygame.key.get_pressed()[pygame.K_DOWN] and ballrect.bottom < height:
        speed[1] = 2
    if pygame.key.get_pressed()[pygame.K_LEFT] and ballrect.left > 0:
        speed[0] = -2
    if pygame.key.get_pressed()[pygame.K_RIGHT] and ballrect.right < width:
        speed[0] = 2
    return

# boundce reverses the speed of a rect if it touches the borders
def bounce(rect, speed):
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
    return

# foodstart checks where the player is and finds an appropriate starting point for food
def foodstart():
    xcoord, ycoord = 10, 10
    if ballrect.center[0] < (width / 2):
        xcoord = width-10
    if ballrect.center[1] < (height / 2):
        ycoord = height-10
    return xcoord, ycoord

# checkcollide checks if the player is colliding with an obstacle
def checkcollide():
    for obst in obstacles:
        if ballrect.colliderect(obst):
            return True
    return False

def increasespeed(speed):
    if speed[0] < 0:
        speed[0] -= 1
    else:
        speed[0] += 1
    if speed[1] < 0:
        speed[1] -= 1
    else: speed[1] += 1

def quit():
    print("Game ended!")
    print("Final score:", score, "points!")
    sys.exit()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    playerspeed = [0, 0]
    setspeed(playerspeed)
    ballrect = ballrect.move(playerspeed)

    if ballrect.colliderect(foodrect):
        score += 100
        xcoord, ycoord = foodstart()
        foodrect.center = (xcoord, ycoord)
        increasespeed(foodspeed)

    if checkcollide():
        quit()
        
    bounce(foodrect, foodspeed)
    foodrect = foodrect.move(foodspeed)

    screen.fill(black)
    for obst in obstacles:
        screen.blit(obstacle, obst)
    screen.blit(food, foodrect)
    screen.blit(ball, ballrect)
    pygame.display.flip()