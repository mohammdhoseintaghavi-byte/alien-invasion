import pygame
from pygame.sprite import Sprite
from paths import IMAGES_DIR
class Boss(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load(str(IMAGES_DIR/"boss.bmp"))
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.screen.get_rect().centerx,50)
        self.x=float(self.rect.x)
        self.max_health = 30 + (ai_game.stats.level // 5) * 20
        self.health = self.max_health
        self.speed = 3 + (ai_game.stats.level // 5)
        self.direction = 1
    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
        if self.rect.right >= self.screen.get_rect().right:
            self.direction=-1
        if self.rect.left<=0:
            self.direction=1
    def blitme(self):
        self.screen.blit(self.image,self.rect)
