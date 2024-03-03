import pygame as pg
import sys
import pymunk as pm
import pymunk.pygame_util
import math

pymunk.pygame_util.positive_y_is_up = False

#параметры PyGame
RES = WIDTH, HEIGHT = 900, 720
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

#настройки Pymunk
space = pymunk.Space()
space.gravity = 0, 0

#Статическая платформа
segment_shape = pymunk.Segment(space.static_body, (2, HEIGHT), (WIDTH, HEIGHT), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

#Динамический куб
class Cube():
    def __init__(self, pos):
        super().__init__()
        self.mass = 1
        self.size = (60,60)

        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos

        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 0.01
        self.shape.friction = 1.0
        self.shape.color = (255,255,255,255)
        space.add(self.body, self.shape)
cube = Cube((300,400))

#Кинетическая машина
class Robot():
    def __init__(self, pos):
        super().__init__()
        self.mass = 100
        self.size = (60,60)
        self.speed = 100
        self.rotation_speed = math.pi/180
        

        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos
        self.body.angle = math.pi

        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 1
        self.shape.friction = 1.0
        self.shape.color = (255,0,0,150)
        
        print(self.body.angle)

        space.add(self.body, self.shape)

    def forward(self):
        # Calculate the movement vector based on the current rotation angle
        x_vel = math.cos(self.body.angle) * self.speed
        y_vel = math.sin(self.body.angle) * self.speed
        self.body.velocity = (x_vel,y_vel)
    
    def backward(self):
        # Calculate the movement vector based on the current rotation angle (backward)
        x_vel = math.cos(self.body.angle+math.pi) * self.speed
        y_vel = math.sin(self.body.angle+math.pi) * self.speed
        self.body.velocity = (x_vel,y_vel)
    
    def rotate_right(self):
        self.body.angle += self.rotation_speed  # Turn right

    def rotate_left(self):
        self.body.angle -= self.rotation_speed  # Turn left 

    def stop(self):
        self.body.velocity = (0,0)   
        self.body.angular_velocity = 0

robot = Robot((WIDTH/2,HEIGHT/2))

#Отрисовка
# Main game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Recieve game inputs
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        robot.rotate_left()
    elif keys[pg.K_RIGHT]:
        robot.rotate_right()

    if keys[pg.K_UP]:
        robot.forward()   
    elif keys[pg.K_DOWN]:
        robot.backward()
    else:
        robot.stop()

    cube.body.velocity *= 0.8
    cube.body.angular_velocity *= 0.8

    print(robot.body.angle)

    surface.fill(pg.Color('black'))

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)
