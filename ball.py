import pygame
import random


class Ball(pygame.sprite.Sprite):
    """A class to manage ball behaviour"""

    def __init__(self, ball_color, screen_width, screen_height):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(ball_color)
        self.rect = self.surf.get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2
        self.speed_x = 4
        self.speed_y = 4

    def move(self):
        """Move ball constantly by x and y axis speed"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_from_wall(self, screen_height, play, sound, hit_list):
        """Change ball y direction after hitting top or bottom wall"""
        if self.rect.y >= screen_height - 20:
            play(sound(random.choice(hit_list)))
            self.speed_y *= -1
        elif self.rect.y < 0:
            play(sound(random.choice(hit_list)))
            self.speed_y *= -1

    def change_x_direction(self):
        """Change the x direction (left/right) of ball"""
        self.speed_x *= -1

    def increase_ball_speed(self):
        """Increase ball speed"""
        self.speed_x *= 1.05
        self.speed_y *= 1.05

    def die(self, screen_width):
        """Remove the ball from screen"""
        if self.rect.x < 0 or self.rect.x > screen_width:
            self.kill()

    def randomize_move_direction(self):
        """Change the x and y direction of ball after removal"""
        num_list = [0, 1, 2]
        if random.choice(num_list) == 0:
            self.speed_x *= -1
        elif random.choice(num_list) == 1:
            self.speed_x *= -1
            self.speed_y *= -1
        elif random.choice(num_list) == 2:
            self.speed_y *= -1
