import pygame
import dialogue_handler

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

def run():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Interstellar Tech Support")
    
    done = False
    clock = pygame.time.Clock()
    
    DH = dialogue_handler.DialogueHandler("dialogue.txt")
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    
        screen.fill((0, 0, 0))
        pygame.display.flip()
        
    pygame.quit()
    
if __name__ == "__main__":
    run()