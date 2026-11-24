import json
import sys
from time import sleep
from winsound import PlaySound
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from boss import Boss
from boss_bullet import BossBullet
from paths import SOUNDS_DIR, HIGH_SCORE_FILE
class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.boss=None
        self.boss_bullets = pygame.sprite.Group()
        self.boss_fire_delay=0

        self._create_fleet()
        self.game_active=False
        self.play=False
        self.game_over=False
        self.easy_button=Button(self,'Easy')
        self.medium_button=Button(self,'Medium')
        self.hard_button=Button(self,'Hard')
        self.easy_button.rect.center = (600,250)
        self.easy_button.msg_image_rect.center=self.easy_button.rect.center
        self.medium_button.rect.center = (600,330)
        self.medium_button.msg_image_rect.center=self.medium_button.rect.center
        self.hard_button.rect.center = (600,410)
        self.hard_button.msg_image_rect.center=self.hard_button.rect.center
        self.shoot_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "shoot.wav"))
        self.explosion_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "explosion.wav"))
        self.hit_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "hit.wav"))
        self.gameover_sound = pygame.mixer.Sound(str(SOUNDS_DIR / "game_over.wav"))
        self.shoot_sound.set_volume(0.3)
        self.explosion_sound.set_volume(0.5)
        self.hit_sound.set_volume(0.5)
        self.gameover_sound.set_volume(0.7)
        self.game_over_font = pygame.font.SysFont(None,100)
        self.info_font = pygame.font.SysFont(None,50)
    def run_game(self):
	    while True:
                self._check_events()
                if self.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_boss_bullets()
                    self._update_aliens()
                self._update_screen()
                self.clock.tick(60)
                if self.boss:
                    self.boss.update()
                    self.boss_fire_delay+=1
                    if self.boss_fire_delay>=40:
                        self._fire_boss_bullet()
                        self.boss_fire_delay=0
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open(HIGH_SCORE_FILE, 'w') as f:
                    json.dump(self.stats.high_score, f)
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if self.game_over:
                        self._start_game()
                    else:
                        self.play=True
                        self._c_p_b(self.play)
                else:
                    self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self,mouse_pos,):
        easy_clicked=self.easy_button.rect.collidepoint(mouse_pos)
        medium_clicked=self.medium_button.rect.collidepoint(mouse_pos)
        hard_clicked=self.hard_button.rect.collidepoint(mouse_pos)
        if easy_clicked and not self.game_active:
            self.settings.difficulty='easy'
            self._start_game()
        elif medium_clicked and not self.game_active:
            self.settings.difficulty='medium'
            self._start_game()
        elif hard_clicked and not self.game_active:
            self.settings.difficulty='hard'
            self._start_game()
    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_images()
        self.game_active=True
        self.game_over=False
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
    def _c_p_b(self,play):
        if play and not self.game_active:
            self.stats.reset_stats()
            self.game_active=True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump(self.stats.high_score, f)
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            self.shoot_sound.play()
    def _fire_boss_bullet(self):
        if self.boss:
            bullet = BossBullet(self)
            self.boss_bullets.add(bullet)
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()
            self._check_bullet_boss_collision()
    def _update_boss_bullets(self):
        self.boss_bullets.update()
        for bullet in self.boss_bullets.copy():
             if bullet.rect.top >= self.settings.screen_height:
                 self.boss_bullets.remove(bullet)
        if pygame.sprite.spritecollideany(self.ship,self.boss_bullets):
            self.boss_bullets.empty()
            self._ship_hit()
    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)
        if collisions:
            for aliens in collisions.values():
                self.explosion_sound.play()
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.stats.score+=self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens and not self.boss:
            self._start_new_level()
    def _check_bullet_boss_collision(self):
        if not self.boss:
            return
        hits = pygame.sprite.spritecollide(self.boss,self.bullets,True)
        if hits:
            self.boss.health -= len(hits)
            if self.boss.health <= 0:
                self.stats.score += 500 * (self.stats.level//5)
                self.sb.prep_score()
                self.boss = None
                self._start_new_level()

    def _start_new_level(self):
        self.bullets.empty()
        self.aliens.empty()
        self.boss = None
        self.stats.level+=1
        self.sb.prep_level()
        self.settings.increase_speed()
        if self.stats.level %5 == 0:
            self.aliens.empty()
            self._create_boss()
        else:
            self.boss = None
            self._create_fleet()
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
        if self.boss:
            if pygame.sprite.collide_rect(self.ship,self.boss):
                self._ship_hit()
    def _ship_hit(self):
        self.hit_sound.play()
        if self.stats.ship_left > 0:
            self.stats.ship_left-=1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.gameover_sound.play()
            self.bullets.empty()
            self.aliens.empty()
            self.boss=None
            self.boss_bullets.empty()
            self.game_active=False
            self.game_over=True
            self.play=False
            pygame.mouse.set_visible(True)
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size

        current_x,current_y=alien_width,alien_height
        while current_y < (self.settings.screen_height-3*alien_height):
            while current_x < (self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=2*alien_width

            current_x=alien_width
            current_y += 2*alien_height
    def _create_alien(self,x_position,y_position):
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)
    def _create_boss(self):
        self.boss=Boss(self)
    def show_game_over(self):
        game_over_image = self.game_over_font.render(
            "GAME OVER",True,(250,0,0))
        game_over_rect=game_over_image.get_rect()
        game_over_rect.center = (self.screen.get_rect().centerx,self.screen.get_rect().centery-80)
        score_image=self.info_font.render(f"Final score:{self.stats.score}",True,(255,255,255))
        score_rect = score_image.get_rect()
        score_rect.center = (self.screen.get_rect().centerx,
                             self.screen.get_rect().centery)
        high_score_image = self.info_font.render(
            f"High Score:{self.stats.high_score}",True,(255,255,255))
        high_score_rect = high_score_image.get_rect()
        high_score_rect.center = (self.screen.get_rect().centerx,
                                  self.screen.get_rect().centery+50)
        restart_image = self.info_font.render(
            "press p to play again",True,(255,255,0))
        restart_rect = restart_image.get_rect()
        restart_rect.center = (
            self.screen.get_rect().centerx,self.screen.get_rect().centery+120)
        self.screen.blit(game_over_image,game_over_rect)
        self.screen.blit(score_image,score_rect)
        self.screen.blit(high_score_image,high_score_rect)
        self.screen.blit(restart_image,restart_rect)
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.boss_bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            if self.game_over:
                self.show_game_over()
            else:
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()
        if self.boss:
            self.boss.blitme()
            pygame.draw.rect(self.screen,(255,0,0),(20,20,300,20))
            current_width = (self.boss.health/self.boss.max_health) * 300
            pygame.draw.rect(self.screen,(0,255,0),(20,20,current_width,20))
        if self.boss:
            text = self.info_font.render(
                f"Boss HP: {self.boss.health}", True, (255, 0, 0))
            self.screen.blit(text, (20, 20))

        pygame.display.flip()




if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()

    