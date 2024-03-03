import pymunk
import pymunk.pygame_util
import pygame
from pygame.locals import QUIT
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Create a point (a small circle) and add it to the space
    point_mass = 1
    point_radius = 5
    point_moment = pymunk.moment_for_circle(point_mass, 0, point_radius)
    point_body = pymunk.Body(point_mass, point_moment)
    point_body.position = (300, 300)
    point_shape = pymunk.Circle(point_body, point_radius)
    space.add(point_body, point_shape)

    # Create a cube and add it to the space
    cube_width = 50
    cube_height = 50
    cube_mass = 1
    cube_moment = pymunk.moment_for_box(cube_mass, (cube_width, cube_height))
    cube_body = pymunk.Body(cube_mass, cube_moment)
    cube_body.position = (400, 400)
    cube_shape = pymunk.Poly.create_box(cube_body, (cube_width, cube_height))
    space.add(cube_body, cube_shape)

    # Define collision handler
    def collision_handler(arbiter, space, data):
        print("Point-Cube Collision Detected!")

    handler = space.add_collision_handler(0, 0)  # Collision type for the point and cube
    handler.data["callback"] = collision_handler

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        space.step(1 / 60.0)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
