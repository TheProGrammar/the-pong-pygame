import pygame


class Scoreboard:
    """A class to manage displaying scores on screen"""

    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.basic_font = pygame.font.Font('C:\Windows\Fonts\calibri.ttf', 32)

    def draw_scores(self, color, screen, screen_width):
        player_text = self.basic_font.render(f'{self.player_score}', False, color)
        screen.blit(player_text, (screen_width / 2 - 30, 290))

        opponent_text = self.basic_font.render(f'{self.ai_score}', False, color)
        screen.blit(opponent_text, (screen_width / 2 + 13, 290))
