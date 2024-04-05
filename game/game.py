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
    space.step(1)

    robot_angle = int(360*game.robot.body.angle/(2*math.pi))
    if robot_angle > 360: robot_angle= robot_angle-360
    if robot_angle < 0: robot_angle= robot_angle+360
    print(robot_angle)
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