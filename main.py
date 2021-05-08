import pygame
from pygame.locals import *
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

# Initiate Pygame
pygame.init()

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Pong Game")

# Set FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
DARK_GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)


# Instantiate objects
r_paddle = Paddle(730, 250, WHITE)
ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
l_paddle = Paddle(50, 250, WHITE)
scoreboard = Scoreboard()

# Create groups to hold ball objects
ball_group = pygame.sprite.Group()
ball_group.add(ball)

# Main Game Loop
running = True
while running:
    clock.tick(FPS)

    # Check for game closing commands
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    # Check for player movement input
    r_paddle.move(6, SCREEN_HEIGHT)

    # Move the ball constantly
    ball.move()

    # Move AI (left) paddle to ball y coordinate
    l_paddle.ai_move(ball, SCREEN_HEIGHT)

    # Check for collision between ball and top/bottom wall
    # Change direction after they collide
    ball.bounce_from_wall(SCREEN_HEIGHT)

    # Check for collision between paddles and ball
    # Change ball direction dependently on collision side
    # Speed up the ball after each contact with paddles
    if ball.rect.colliderect(r_paddle.rect) or ball.rect.colliderect(l_paddle.rect):
        if abs(ball.rect.right - r_paddle.rect.left) < 10 and ball.speed_x > 0 or \
                abs(ball.rect.left - l_paddle.rect.right) < 10 and ball.speed_x < 0:
            ball.increase_ball_speed()
            ball.change_x_direction()
        if abs(ball.rect.top - r_paddle.rect.bottom) < 20 and ball.speed_y < 0:
            ball.increase_ball_speed()
            ball.speed_y *= -1
        if abs(ball.rect.bottom - r_paddle.rect.top) < 20 and ball.speed_y > 0:
            ball.increase_ball_speed()
            ball.speed_y *= -1

    # Check if ball is outside of screen
    # Add score
    # Create a new ball and change ball x direction
    if ball.rect.x < 0:
        scoreboard.ai_score += 1
        ball.die(SCREEN_WIDTH)
        ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
        ball.randomize_move_direction()

    elif ball.rect.x > SCREEN_WIDTH:
        scoreboard.player_score += 1
        ball.die(SCREEN_WIDTH)
        ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
        ball.randomize_move_direction()

    # Fill the screen with color
    screen.fill(DARK_GRAY)

    # Draw a line on the middle of screen
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), 1)

    # Draw object on screen each frame
    screen.blit(r_paddle.surf, r_paddle.rect)
    screen.blit(ball.surf, ball.rect)
    screen.blit(l_paddle.surf, l_paddle.rect)

    # Draw score
    scoreboard.draw_scores(LIGHT_GRAY, screen, SCREEN_WIDTH)

    # Refresh the screen
    pygame.display.flip()

pygame.quit()
