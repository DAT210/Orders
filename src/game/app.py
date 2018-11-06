import sys, pygame
pygame.init()

class Object:
    def __init__(self, rect, speed):
        self.rect = rect
        self.speed = speed

screen_width, screen_height = 1920, 1080

scoreboard_height = 50
width, height = screen_width, screen_height-scoreboard_height
size = screen_width, screen_height
black = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
pygame.mouse.set_visible(False)

scoreboard = pygame.Surface((width, scoreboard_height))
scoreboard.fill([100, 100, 100])

# Fonts used for different kinds of text
score_font = pygame.font.SysFont("monospace", scoreboard_height)
headline_font = pygame.font.SysFont("monospace", 200)
menu_font = pygame.font.SysFont("monospace", 150)

# Text used for the pause menu
paused_text = headline_font.render("Paused", 1, (255, 255, 255))
paused_rect = paused_text.get_rect()
resume_text = menu_font.render("Resume", 1, (100, 100, 100))
resume_rect = resume_text.get_rect()
quit_text = menu_font.render("Quit", 1, (100, 100, 100))
quit_rect = quit_text.get_rect()
resume_text_selected = menu_font.render("Resume", 1, (255, 255, 255))
resume_selected_rect = resume_text.get_rect()
quit_text_selected = menu_font.render("Quit", 1, (255, 255, 255))
quit_selected_rect = quit_text.get_rect()

# Pause menu text placement
paused_rect.center = (width/2, height/4)
resume_rect.center = resume_selected_rect.center = (width/2, height/2)
quit_rect.center = quit_selected_rect.center = (width/2, 3*height/4)

# Text used for the game over menu
game_over_text = headline_font.render("Game over!", 1, (255, 255, 255))
game_over_rect = game_over_text.get_rect()
play_again_text = menu_font.render("Play again", 1, (100, 100, 100))
play_again_rect = play_again_text.get_rect()
exit_game_text = menu_font.render("Exit game", 1, (100, 100, 100))
exit_game_rect = exit_game_text.get_rect()
play_again_text_selected = menu_font.render("Play again", 1, (255, 255, 255))
play_again_selected_rect = play_again_text.get_rect()
exit_game_text_selected = menu_font.render("Exit game", 1, (255, 255, 255))
exit_game_selected_rect = exit_game_text.get_rect()

# Game over menu text placement
game_over_rect.center = (width/2, height/5)
play_again_rect.center = play_again_selected_rect.center = (width/2, 3*height/5)
exit_game_rect.center = exit_game_selected_rect.center = (width/2, 4*height/5)

ball_right = pygame.image.load("images/player_right.gif")
ball_left = pygame.image.load("images/player_left.gif")
ball_up = pygame.image.load("images/player_up.gif")
ball_down = pygame.image.load("images/player_down.gif")
ball_upright = pygame.image.load("images/player_upright.gif")
ball_upleft = pygame.image.load("images/player_upleft.gif")
ball_downright = pygame.image.load("images/player_downright.gif")
ball_downleft = pygame.image.load("images/player_downleft.gif")
foodimage = pygame.image.load("images/food.png")
obstacle = pygame.image.load("images/big_obstacle.png")

player = Object(ball_downright.get_rect(), [0, 0])
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

player_image = ball_downright

score = 0

print("Game started!")

# set_player_speed sets speed based on arrow keys pressed
def set_player_speed():
    if pygame.key.get_pressed()[pygame.K_UP] and player.rect.top > 0:
        player.speed[1] = -3
    if pygame.key.get_pressed()[pygame.K_DOWN] and player.rect.bottom < height-1:
        player.speed[1] = 3
    if pygame.key.get_pressed()[pygame.K_LEFT] and player.rect.left > 0:
        player.speed[0] = -3
    if pygame.key.get_pressed()[pygame.K_RIGHT] and player.rect.right < width:
        player.speed[0] = 3
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

# increase_speed increases speed input by 1 in x and y direction
def increase_speed(speed):
    if speed[0] < 0:
        speed[0] -= 1
    else:
        speed[0] += 1
    if speed[1] < 0:
        speed[1] -= 1
    else:
        speed[1] += 1

def restart_game():
    global score
    score = 0

    player.rect.topleft = [0, 0]

    food.rect.topright = [width, 0]
    food.speed = [-1, -1]

    obstacles["topleft"].rect.center = (width/4, height/4)
    obstacles["bottomright"].rect.center = (3*width/4, 3*height/4)
    obstacles["topright"].rect.center = (3*width/4, height/4)
    obstacles["bottomleft"].rect.center = (width/4, 3*height/4)

    obstacles["topleft"].speed = [0, -2]
    obstacles["bottomright"].speed = [0, 2]
    obstacles["topright"].speed = [2, 0]
    obstacles["bottomleft"].speed = [-2, 0]
    
    if "top" in obstacles:
        obstacles.pop("top")
    if "bottom" in obstacles:
        obstacles.pop("bottom")
    if "right" in obstacles:
        obstacles.pop("right")
    if "left" in obstacles:
        obstacles.pop("left")

def choose_player(speed):
    if speed[0] > 0 and speed[1] == 0:
        return ball_right
    if speed[0] < 0 and speed[1] == 0:
        return ball_left
    if speed[0] == 0 and speed[1] > 0:
        return ball_down
    if speed[0] == 0 and speed[1] < 0:
        return ball_up
    if speed[0] > 0 and speed[1] > 0:
        return ball_downright
    if speed[0] < 0 and speed[1] < 0:
        return ball_upleft
    if speed[0] > 0 and speed[1] < 0:
        return ball_upright
    if speed[0] < 0 and speed[1] > 0:
        return ball_downleft
    else:
        return ball_downright

def quit_game():
    final_score_text = menu_font.render("Final score: " + str(score), 1, (255, 255, 255))
    final_score_rect = final_score_text.get_rect()
    final_score_rect.center = (width/2, 2*height/5)
    
    # 0 = resume, 1 = exit
    selected = 0

    while 1: 
        pygame.event.pump()

        if pygame.key.get_pressed()[pygame.K_UP]:
            selected = 0
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            selected = 1

        if selected is 0:
            screen.fill(black)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            screen.blit(play_again_text_selected, play_again_selected_rect)
            screen.blit(exit_game_text, exit_game_rect)
            pygame.display.flip()
        elif selected is 1:
            screen.fill(black)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            screen.blit(play_again_text, play_again_rect)
            screen.blit(exit_game_text_selected, exit_game_selected_rect)
            pygame.display.flip()

        if selected is 0 and pygame.key.get_pressed()[pygame.K_RETURN]:
            restart_game()
            break
            
        if selected is 1 and pygame.key.get_pressed()[pygame.K_RETURN]:
            print("Exiting game")
            print("Final score: " + str(score))
            sys.exit()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Pressing escape pauses the game
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        # 0 = resume, 1 = quit
        selected = 0
        
        # Pause loop
        while 1:
            pygame.event.pump()

            if pygame.key.get_pressed()[pygame.K_UP]:
                selected = 0
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                selected = 1

            if selected is 0:
                screen.blit(paused_text, paused_rect)
                screen.blit(resume_text_selected, resume_selected_rect)
                screen.blit(quit_text, quit_rect)
                pygame.display.flip()
            elif selected is 1:
                screen.blit(paused_text, paused_rect)
                screen.blit(resume_text, resume_rect)
                screen.blit(quit_text_selected, quit_selected_rect)
                pygame.display.flip()

            if selected is 0 and pygame.key.get_pressed()[pygame.K_RETURN]:
                break
            
            if selected is 1 and pygame.key.get_pressed()[pygame.K_RETURN]:
                sys.exit()
            
    player.speed = [0, 0]
    set_player_speed()

    player.rect = player.rect.move(player.speed)

    if player.rect.colliderect(food.rect):
        score += 100

        if score == 1000:
            obstacles["top"] = Object(obstacle.get_rect(), [0, 0])
            obstacles["bottom"] = Object(obstacle.get_rect(), [0, 0])
            obstacles["right"] = Object(obstacle.get_rect(), [0, 0])
            obstacles["left"] = Object(obstacle.get_rect(), [0, 0])
            if player.rect.center[0] < (width / 2):
                obstacles["top"].rect.topright = (width, height/4)
                obstacles["top"].speed = [-2, 0]
                obstacles["bottom"].rect.bottomright = (width, 3*height/4)
                obstacles["bottom"].speed = [-2, 0]
            else:
                obstacles["top"].rect.topleft = (0, height/4)
                obstacles["top"].speed = [2, 0]
                obstacles["bottom"].rect.bottomleft = (0, 3*height/4)
                obstacles["bottom"].speed = [2, 0]

            if player.rect.center[1] < (height / 2):
                obstacles["right"].rect.bottomright = (3*width/4, height)
                obstacles["right"].speed = [0, -2]
                obstacles["left"].rect.bottomleft = (width/4, height)
                obstacles["left"].speed = [0, -2]
            else:
                obstacles["right"].rect.topright = (3*width/4, 0)
                obstacles["right"].speed = [0, 2]
                obstacles["left"].rect.topleft = (width/4, 0)
                obstacles["left"].speed = [0, 2]

        xcoord, ycoord = foodstart()
        food.rect.center = (xcoord, ycoord)
        if (food.speed[0]**(2.0)+food.speed[1]**(2.0))**(0.5) < 5.0:
            increase_speed(food.speed)
        for key in obstacles:
            if key == "top" or key == "bottom" or key == "right" or key == "left":
                continue
            obstacles[key].speed = [obstacles[key].speed[1], obstacles[key].speed[0]]

    bounce(food.rect, food.speed)
    food.rect = food.rect.move(food.speed)

    screen.fill(black)
    screen.blit(scoreboard, [0, height])

    if player.speed != [0, 0]:
        player_image = choose_player(player.speed)

    screen.blit(player_image, player.rect)

    score_text = score_font.render("Score: " + str(score), 1, (255,255,255))
    score_rect = score_text.get_rect()
    score_rect.bottomleft = (0, screen_height)
    screen.blit(score_text, score_rect)

    for key in obstacles:
        obstacles[key].rect = obstacles[key].rect.move(obstacles[key].speed)
        bounce(obstacles[key].rect, obstacles[key].speed)
        screen.blit(obstacle, obstacles[key].rect)
    
    screen.blit(foodimage, food.rect)

    pygame.display.flip()

    if is_collision():
        quit_game()
