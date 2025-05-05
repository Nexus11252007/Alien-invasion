import sys
import pygame
from rocket import Rocket
class RocketGame:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((1200,600))
        pygame.display.set_caption("Rocket")
        self.bg_color=(230,230,230)
        self.rocket=Rocket(self)
    def run_game(self):
        while True:
            self._check_events()
            self.rocket.update()
            self._update_screen()     
                
                    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_for_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_for_keyup_events(event)
    def _check_for_keydown_events(self,event):
        if event.key==pygame.K_UP:
            self.rocket.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.rocket.moving_down=True
        elif event.key==pygame.K_LEFT:
            self.rocket.moving_left=True
        elif event.key==pygame.K_RIGHT:
            self.rocket._moving_right=True
        elif event.key==pygame.K_q:
            sys.exit()
    def _check_for_keyup_events(self,event):
        if event.key==pygame.K_UP:
            self.rocket.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.rocket.moving_down=False
        elif event.key==pygame.K_LEFT:
            self.rocket.moving_left=False
        elif event.key==pygame.K_RIGHT:
            self.rocket._moving_right=False
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.rocket.blitme()
        pygame.display.flip()
if __name__=='__main__':
    ai=RocketGame()
    ai.run_game()
    