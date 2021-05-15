import pygame
from pygame import *


class Paddle:
    """A class to manage player behaviour"""

    def __init__(self, x, y, white):
        self.surf = pygame.Surface((25, 120))
        self.surf.fill(white)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, speed, s_height):
        """Move player paddle dependently on key input"""
        if pygame.key.get_pressed()[K_UP]:
            self.rect.y -= speed
        if pygame.key.get_pressed()[K_DOWN]:
            self.rect.y += speed

        # Limit paddle movement within screen
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= s_height:
            self.rect.bottom = s_height

    def ai_move(self, ball, s_height, speed):
        """Function that moves left (AI) paddle towards
        the y position of ball automatically"""
        if ball.speed_x <= 0 and self.rect.centery < ball.rect.centery:
            self.rect.centery += speed
        elif self.rect.centery > ball.rect.centery:
            self.rect.centery -= speed

        # Moves left paddle to the center of the screen after ball contact
        if ball.speed_x > 0:
            y_difference = s_height / 2 - self.rect.centery
            new_paddle_y = y_difference / 30
            self.rect.centery += new_paddle_y

        # Limit paddle movement within screen
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= s_height:
            self.rect.bottom = s_height
