from classes import * 
import sys
import time

game = Game()
game.reset_game()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            time.sleep(300/1000)
            game.do_event(event.key)

    # Recieve game inputs
    keys = pygame.key.get_pressed()
    game.do_event(keys)
    # Drow objects on screen
    game.draw()
    pygame.display.flip()
    # Control the frame rate
    clock.tick(4)