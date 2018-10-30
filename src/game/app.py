import sys, pygame
pygame.init()

class Object:
    def __init__(self, rect, speed):
        self.rect = rect
        self.speed = speed

screen_width, screen_height = 1500, 1000

scoreboard_height = 50
width, height = screen_width, screen_height-scoreboard_height
size = screen_width, screen_height
black = 0, 0, 0
screen = pygame.display.set_mode(size)

scoreboard = pygame.Surface((width, scoreboard_height))
scoreboard.fill([100, 100, 100])
textfont = pygame.font.SysFont("monospace", 50)

ball = pygame.image.load("images/intro_ball.gif")
foodimage = pygame.image.load("images/food.png")
obstacle = pygame.image.load("images/big_obstacle.png")

player = Object(ball.get_rect(), [0, 0])
food = Object(foodimage.get_rect(), [-1, -1])
food.rect.topright = (width, 0)

obstacles = {
    "center": Object(obstacle.get_rect(), [0, 0]),
    "topleft": Object(obstacle.get_rect(), [0, -2]),
    "bottomright": Object(obstacle.get_rect(), [0, 2]),
    "topright": Object(obstacle.get_rect(), [2, 0]),
    "bottomleft": Object(obstacle.get_rect(), [-2, 0])
}

obstacles["center"].rect.center = (width/2, height/2)
obstacles["topleft"].rect.center = (width/4, height/4)
obstacles["bottomright"].rect.center = (3*width/4, 3*height/4)
obstacles["topright"].rect.center = (3*width/4, height/4)
obstacles["bottomleft"].rect.center = (width/4, 3*height/4)

score = 0

print("Game started!")

# set_player_speed sets speed based on arrow keys pressed
def set_player_speed():
    if pygame.key.get_pressed()[pygame.K_UP] and player.rect.top > 0:
        player.speed[1] = -2
    if pygame.key.get_pressed()[pygame.K_DOWN] and player.rect.bottom < height:
        player.speed[1] = 2
    if pygame.key.get_pressed()[pygame.K_LEFT] and player.rect.left > 0:
        player.speed[0] = -2
    if pygame.key.get_pressed()[pygame.K_RIGHT] and player.rect.right < width:
        player.speed[0] = 2
    return

# bounce reverses the speed of a rect if it touches the borders
def bounce(rect, speed):
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
    return

# foodstart checks where the player is and finds an appropriate starting point for food
def foodstart():
    xcoord, ycoord = 10, 10
    if player.rect.center[0] < (width / 2):
        xcoord = width-10
    if player.rect.center[1] < (height / 2):
        ycoord = height-10
    return xcoord, ycoord

# iscollision checks if the player is colliding with an obstacle
def is_collision():
    for key in obstacles:
        if player.rect.colliderect(obstacles[key].rect):
            return True
    return False

def increase_speed(speed):
    if speed[0] < 0:
        speed[0] -= 1
    else:
        speed[0] += 1
    if speed[1] < 0:
        speed[1] -= 1
    else:
        speed[1] += 1

def quit_game():
    print("Game ended!")
    print("Final score:", score, "points!")
    sys.exit()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    player.speed = [0, 0]
    set_player_speed()

    player.rect = player.rect.move(player.speed)

    if player.rect.colliderect(food.rect):
        score += 100
        xcoord, ycoord = foodstart()
        food.rect.center = (xcoord, ycoord)
        if (food.speed[0]**(2.0)+food.speed[1]**(2.0))**(0.5) < 5.0:
            increase_speed(food.speed)

    if is_collision():
        quit_game()

    bounce(food.rect, food.speed)
    food.rect = food.rect.move(food.speed)

    screen.fill(black)
    screen.blit(scoreboard, [0, height])

    score_text = textfont.render("Score: " + str(score), 1, (255,255,255))
    screen.blit(score_text, (0, height))

    for key in obstacles:
        obstacles[key].rect = obstacles[key].rect.move(obstacles[key].speed)
        bounce(obstacles[key].rect, obstacles[key].speed)
        screen.blit(obstacle, obstacles[key].rect)
    
    screen.blit(foodimage, food.rect)
    screen.blit(ball, player.rect)
    pygame.display.flip()
