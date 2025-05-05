import sys
import pygame

class KeyDetector:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((900,300),)
        self.bg_color=(230,230,230)
        pygame.display.set_caption("Key Detector")

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        sys.exit()
                    else:
                        print(event.key)
            self.screen.fill(self.bg_color)
            pygame.display.flip()
if __name__=="__main__":
    ai=KeyDetector()
    ai.run_game()