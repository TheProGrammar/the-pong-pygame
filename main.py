import random
import time

import pygame
from pygame.locals import *
import tkinter
from tkinter import simpledialog
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

# Initiate Pygame
pygame.init()

# Initiate Mixer/Sound Settings
pygame.mixer.init()
play = pygame.mixer.Sound.play
sound = pygame.mixer.Sound
hit_list = ['sounds/hit1.wav', 'sounds/hit2.wav', 'sounds/hit3.wav', 'sounds/hit4.wav']

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
r_paddle = Paddle(SCREEN_WIDTH - (SCREEN_WIDTH * 0.1), SCREEN_HEIGHT / 2 - 50, WHITE)
ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
l_paddle = Paddle(SCREEN_WIDTH * 0.07, SCREEN_HEIGHT / 2 - 50, WHITE)
scoreboard = Scoreboard()

# Create groups to hold ball objects
ball_group = pygame.sprite.Group()
ball_group.add(ball)

# Pause Menu Settings
paused = False

# Enemy difficulty
ROOT = tkinter.Tk()
ROOT.withdraw()
USER_INP = int(simpledialog.askstring(title="Difficulty",
                                      prompt="Choose Difficulty. 1 = Easy, 2 = Normal, 3 = Hard"))

ai_speed = 0
player_speed = 0

if USER_INP == 1:
    ai_speed = 3
    player_speed = 7
elif USER_INP == 2:
    ai_speed = 5
    player_speed = 6
else:
    ai_speed = 6
    player_speed = 5

time.sleep(1)

# Main Game Loop
running = True
while running:

    # Check for game closing commands
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_p:
                paused = not paused
                play(sound('sounds/pause.wav'))
        elif event.type == QUIT:
            running = False

    while paused:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    paused = False
                    play(sound('sounds/pause.wav'))

    # Check for player movement input
    r_paddle.move(player_speed, SCREEN_HEIGHT)

    # Move the ball constantly
    ball.move()

    # Move AI (left) paddle to ball y coordinate
    l_paddle.ai_move(ball, SCREEN_HEIGHT, ai_speed)

    # Check for collision between ball and top/bottom wall
    # Change direction after they collide
    ball.bounce_from_wall(SCREEN_HEIGHT, play, sound, hit_list)

    # Check for collision between paddles and ball
    # Change ball direction dependently on collision side
    # Speed up the ball after each contact with paddles
    if ball.rect.colliderect(r_paddle.rect) or ball.rect.colliderect(l_paddle.rect):
        if abs(ball.rect.right - r_paddle.rect.left) < 10 and ball.speed_x > 0 or \
                abs(ball.rect.left - l_paddle.rect.right) < 10 and ball.speed_x < 0:
            play(sound(random.choice(hit_list)))
            ball.increase_ball_speed()
            ball.change_x_direction()
        if abs(ball.rect.top - r_paddle.rect.bottom) < 20 and ball.speed_y < 0:
            play(sound(random.choice(hit_list)))
            ball.increase_ball_speed()
            ball.speed_y *= -1
        if abs(ball.rect.bottom - r_paddle.rect.top) < 20 and ball.speed_y > 0:
            play(sound(random.choice(hit_list)))
            ball.increase_ball_speed()
            ball.speed_y *= -1

    # Check if ball is outside of screen
    # Add score
    # Create a new ball and change ball x direction
    if ball.rect.x < 0:
        play(sound('sounds/win.wav'))
        scoreboard.ai_score += 1
        ball.die(SCREEN_WIDTH)
        ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
        ball.randomize_move_direction()

    elif ball.rect.x > SCREEN_WIDTH:
        play(sound('sounds/death.wav'))
        scoreboard.player_score += 1
        ball.die(SCREEN_WIDTH)
        ball = Ball(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)
        ball.randomize_move_direction()

    # Fill the screen with color
    screen.fill(DARK_GRAY)

    # Draw a line on the middle of screen
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), 1)

    # Draw object on screen each frame
    screen.blit(r_paddle.surf, r_paddle.rect)
    screen.blit(ball.surf, ball.rect)
    screen.blit(l_paddle.surf, l_paddle.rect)

    # Draw score
    scoreboard.draw_scores(LIGHT_GRAY, screen, SCREEN_WIDTH)

    # Refresh the screen
    pygame.display.flip()
    # Limits FPS to 60
    clock.tick(FPS)

pygame.quit()
