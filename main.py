import pygame
import desktop
import program

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

def run():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED)
    pygame.display.set_caption("Interstellar Tech Support")
    
    done = False
    clock = pygame.time.Clock()
    
    its_desktop = desktop.Desktop(pygame.Rect(0, 0, *SCREEN_SIZE))

    chat_support_icon = pygame.image.load("res/imgs/ChatIcon.png").convert_alpha()
    chat_program = program.ChatSupport(chat_support_icon)

    laser_program_icon = pygame.image.load("res/imgs/LaserIcon.png").convert_alpha()
    laser_program = program.LaserCommand(laser_program_icon)

    its_desktop.programs.append(chat_program)
    its_desktop.programs.append(laser_program)
    
    while not done:
        # 30 FPS to give a more old school feel
        delta = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Handle ordering of windows
                    its_desktop.detect_window_click(event.pos)
                    
                    # Check if we are clicking on an icon for any of the programs.
                    # NOTE: We can currently open a program if the icon is behind the window
                    for cur_program in its_desktop.programs:
                        if not cur_program.open and not cur_program.opening and cur_program.icon_rect.collidepoint(event.pos):
                            if cur_program.selected:
                                cur_program.launch_program()
                                cur_program.selected = False
                            else:
                                cur_program.selected = True
                        else:
                            cur_program.selected = False
                    
        its_desktop.update(delta)

        screen.fill((0, 0, 0))
        its_desktop.draw(screen, pygame.Rect(0, 0, *SCREEN_SIZE))
        
        pygame.display.flip()
        
    pygame.quit()
    
if __name__ == "__main__":
    run()