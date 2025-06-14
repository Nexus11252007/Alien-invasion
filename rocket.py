import pygame

class Rocket:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pygame.image.load("Images/rocket.bmp")
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        self._moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False
    def update(self):
        if self._moving_right and self.rect.right<self.screen_rect.right:
            self.rect.x+=1
        elif self.moving_left and self.rect.left>0:
            self.rect.x-=1
        elif self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.rect.y+=1
        elif self.moving_up and self.rect.top>0:
            self.rect.y-=1

    def blitme(self):
        self.screen.blit(self.image,self.rect)