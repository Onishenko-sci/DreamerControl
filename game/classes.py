import pygame
from pygame.locals import *

import pymunk
from pymunk.pygame_util import *
from pymunk import Vec2d
import math

pygame.init()
pymunk.pygame_util.positive_y_is_up = False

width, height = 1024, 768
FPS = 60
background = pygame.image.load('./sprites/capture.jpg')
clock = pygame.time.Clock()

pygame.display.set_mode((width, height))
screen = pygame.display.get_surface()
space = pymunk.Space()
space.gravity = 0, 0

draw_options = pymunk.pygame_util.DrawOptions(screen)

class Object:
    def __init__(self, pos):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos
        space.add(self.body)
        Game.objects.append(self)

    def draw(self):
        angle = self.body.angle
        img = pygame.transform.rotate(self.img, -1*math.degrees(angle))

        self.body.velocity = self.body.velocity*0.80
        self.body.angular_velocity = self.body.angular_velocity*0.80

        pos = to_pygame(self.body.position, screen)
        rect = img.get_rect()
        rect.center = to_pygame(self.body.position, screen)
        screen.blit(img, rect)


class Button(Object):
    radius = 40
    img = pygame.image.load('./sprites/Button.png').convert_alpha()
    img = pygame.transform.scale(img, (radius*2, radius*2))
    def __init__(self, pos):
        super().__init__(pos) 
        self.center = pos+ Vec2d(self.radius/2,self.radius/2)
         

class Rectangle(Object):
    def __init__(self, pos):
        super().__init__(pos)
        size = self.img.get_size()
        shape = pymunk.Poly.create_box(self.body, size)
        shape.elasticity = 0
        shape.friction = 0.1
        space.add(shape)


class Cube(Rectangle):
    pic_size = (64, 64)
    img = pygame.image.load('./sprites/cube.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)


class Robot(Object):
    img = pygame.image.load('./sprites/robot.png').convert_alpha()

    def __init__(self, pos):
        super().__init__(pos)
        self.speed = 100
        self.rotation_speed = math.pi/180
        #Init shape
        size = self.img.get_size()
        print(f"Robot size {size}")
        shape = pymunk.Circle(self.body, size[0]/2)
        shape.elasticity = 0
        shape.friction = 0.1
        space.add(shape)
        
    def forward(self):
        # Calculate the movement vector based on the current rotation angle
        x_vel = math.cos(self.body.angle) * self.speed
        y_vel = math.sin(self.body.angle) * self.speed
        self.body.velocity = (x_vel, y_vel)

    def backward(self):
        # Calculate the movement vector based on the current rotation angle (backward)
        x_vel = math.cos(self.body.angle+math.pi) * self.speed
        y_vel = math.sin(self.body.angle+math.pi) * self.speed
        self.body.velocity = (x_vel, y_vel)

    def rotate_right(self):
        self.body.angle += self.rotation_speed  # Turn right

    def rotate_left(self):
        self.body.angle -= self.rotation_speed  # Turn left

    def stop(self):
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0


class Game:
    objects = []
    score = 0
    debug = True

    def __init__(self):
        self.score = 0

    def set_ground(self):
        shape = pymunk.Segment(space.static_body, (0, 10), (1200, 10), 4)
        shape.friction = 1
        shape.collision_type = 3
        space.add(shape)

    def remove_objects(self):
        """Remove all Objectects from space."""
        Game.objects = []
        for body in space.bodies:
            space.remove(body)
        for shape in space.shapes:
            space.remove(shape)

    def draw(self):
        """Draw pymunk Objectects on pygame screen."""
        if self.win_condition():
            self.reset_game()

        screen.blit(background, (0, 0))
        if self.debug:
            space.debug_draw(draw_options)
        for obj in self.objects:
            obj.draw()
        space.step(0.02)

    def win_condition(self):
        dV = self.cube.body.position-self.button.center    
        Distance = math.sqrt(dV[0]**2+dV[1]**2)
        if Distance < self.button.radius:
            return(True)
        return(False)
    
    

    def do_event(self, keys):
        if keys[K_LEFT]:
            self.robot.rotate_left()
        elif keys[K_RIGHT]:
            self.robot.rotate_right()
    
        if keys[K_UP]:
            self.robot.forward()   
        elif keys[K_DOWN]:
            self.robot.backward()
        else:
            self.robot.stop()

        if keys[K_d]:
            self.debug = not self.debug
        
        if keys[K_r]:
            self.reset_game()

    def reset_game(self):
        """Set player level."""
        self.remove_objects()
        self.set_ground()

        self.button = Button((800,600))
        self.robot = Robot((500, 500))
        self.cube = Cube((300,300))
