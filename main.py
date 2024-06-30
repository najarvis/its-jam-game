import pygame
import dialogue_handler
import desktop

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

def run():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Interstellar Tech Support")
    
    done = False
    clock = pygame.time.Clock()
    
    its_desktop = desktop.Desktop(pygame.Rect(0, 0, *SCREEN_SIZE))

    chat_support_icon = pygame.image.load("res/imgs/ChatIcon.png").convert_alpha()
    chat_program = desktop.ChatSupport(chat_support_icon)

    its_desktop.programs.append(chat_program)

    # DH = dialogue_handler.DialogueHandler("dialogue.txt")
    # margin_x = 20
    # margin_y = 10
    # text_rect = pygame.Rect(margin_x, HEIGHT / 2, WIDTH - (margin_x * 2), HEIGHT / 2 - margin_y)
    
    while not done:
        delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for program in its_desktop.programs:
                        program.selected = False
                        if program.rect.collidepoint(event.pos):
                            program.selected = True
                    
        # DH.update(delta)

        screen.fill((0, 0, 0))
        its_desktop.draw(screen, pygame.Rect(0, 0, *SCREEN_SIZE))
        # DH.draw_text(screen, text_rect)

        pygame.display.flip()
        
    pygame.quit()
    
if __name__ == "__main__":
    run()