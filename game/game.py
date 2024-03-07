from classes import * 
import sys

game = Game()
game.reset_game()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Recieve game inputs
    keys = pygame.key.get_pressed()
    game.do_event(keys)
    # Drow objects on screen
    game.draw()
    pygame.display.flip()
    # Control the frame rate
    clock.tick(FPS)