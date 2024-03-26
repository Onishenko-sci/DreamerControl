from classes import * 
import sys
import time

game = Game('laser', 0)
game.reset_game()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            #time.sleep(300/1000)
            game.do_event(event.key)


    # Drow objects on screen
    game.draw()
    space.step(0.1)
    # Win
    if game.win_condition():
        game.reset_game()
        print("Win!")
    # Lose
    if game.lose:
        game.reset_game()
        print("Lose...")
        

    pygame.display.flip()
    # Control the frame rate
    clock.tick(4)