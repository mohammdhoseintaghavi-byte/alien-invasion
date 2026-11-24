import pygame
from pygame.sprite import Sprite

class BossBullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.color = (255, 0, 0)
        self.width = 6
        self.height = 18

        self.rect = pygame.Rect(0, 0,self.width,self.height)

        self.rect.midtop = ai_game.boss.rect.midbottom

        self.y = float(self.rect.y)

    def update(self):
        self.y += 5
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)