import sys

from time import sleep

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienIvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))#,pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        #   and create a scoreboard.
        self.stats=GameStats(self)
        self.sb=Scoreboard(self )

        # Set the background color.
        self.bg_color =(self.settings.bg_color)

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()

        # Make the Play button.
        self.play_button=Button(self,"Play")
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.Update()
                self._update_bullet()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type==pygame.KEYDOWN:
                self._check_for_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_for_keyup_events(event)
    def _check_for_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            #move the ship to the right
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_p:
            self._start_game()
            
    def _check_for_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        if event.key==pygame.K_LEFT:
            self.ship.moving_left=False
        if event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create new bullets and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullet(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        #Get rid of bullets that have dissapeard
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for alien in collisions.values():
                self.stats.score+=self.settings.alien_points*len(alien)
                self.sb.prep_score()
                self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level+=1
            self.sb.prep_level()

            
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width - (2*alien_width)
        number_of_aliens=available_space_x // (2*alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        available_space_y=self.settings.screen_height-(3*alien_height)-self.ship.rect.height
        number_of_rows=available_space_y // (2*alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        """Create an alien and place it in the row."""
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.y = alien_height + 2*alien_height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()

        #look for alien ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

         #Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left>0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ship_left-=1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom>=screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_play_button(self,mouse_pos):
            """Start a new game when the player clicks Play."""
            button_clicked=self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                # Reset the game settings.
                self.settings.initialize_dynamic_settings()
                self._start_game()
                
    
    def _start_game(self):
        #Start the game

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active=True
        self.sb.prep_score()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen """
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        """check if the fleet is at an edge, 
        then update the positions of all the alins in the fleet"""
        self._check_fleet_edges()
        
        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    
if __name__== '__main__':
    # Make a game instance, and run the game.
    ai=AlienIvasion()
    ai.run_game()