import pygame
from pygame.locals import *

import pymunk
from pymunk.pygame_util import *
from pymunk import Vec2d
import math
import random

pygame.init()
pymunk.pygame_util.positive_y_is_up = False

width, height = 640, 480
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
        self.body = pymunk.Body(mass=1, moment=100)
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
    radius = 20
    img = pygame.image.load('./sprites/Button.png').convert_alpha()
    img = pygame.transform.scale(img, (radius*2, radius*2))
    def __init__(self, pos):
        super().__init__(pos) 
        self.center = pos+ Vec2d(self.radius/2,self.radius/2)

class  Laser(Object):
    radius = 10
    img = pygame.image.load('./sprites/laser.jpg').convert_alpha()
    def __init__(self, pos):
        super().__init__(pos) 
        self.center = pos+ Vec2d(2,2)


class Rectangle(Object):
    def __init__(self, pos):
        super().__init__(pos)
        size = self.img.get_size()
        shape = pymunk.Poly.create_box(self.body, size)
        shape.elasticity = 0
        shape.friction = 0.1
        space.add(shape)

class Circle(Object):
    def __init__(self, pos):
        super().__init__(pos)
        size = self.img.get_size()
        shape = pymunk.Circle(self.body, radius = size[0]/2)
        shape.elasticity = 0
        shape.friction = 0.1
        shape.collision_type = 2
        space.add(shape)

class Obstacle(Circle):
    pic_size = (20, 20)
    img = pygame.image.load('./sprites/obstacle0.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)


class Cube(Rectangle):
    pic_size = (32, 32)
    img = pygame.image.load('./sprites/cube.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)


class Robot(Object):
    pic_size = (48, 48)
    img = pygame.image.load('./sprites/robot.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)
        self.speed = 1000
        self.rotation_speed = math.pi/18
        #Init shape
        size = self.img.get_size()
        print(f"Robot size {size}")
        shape = pymunk.Circle(self.body, size[0]/2.5)
        shape.elasticity = 0
        shape.friction = 0.1
        shape.collision_type = 1
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
    obstacles = []
    score = 0
    debug = True
    cube = 0
    laser = 0

    def __init__(self):
        self.score = 0
        space.add_collision_handler(1, 2).begin = self.robot_hit_wall

    def robot_hit_wall(self,arbiter, space, _):
        self.reset_game()
        return True

    def set_ground(self):
        top = pymunk.Segment(space.static_body, (80, 122), (640, 122), 4)
        left = pymunk.Segment(space.static_body, (80, 122), (80, 384), 4)
        bottom = pymunk.Segment(space.static_body, (80, 384), (640, 395), 4)
        walls = [top,left,bottom]
        for wall in walls:
            wall.collision_type = 2
            space.add(wall)

    def remove_objects(self):
        """Remove all Objectects from space."""
        Game.objects = []
        for body in space.bodies:
            space.remove(body)
        for shape in space.shapes:
            space.remove(shape)

    def draw(self):
        """Draw pymunk Objectects on pygame screen."""
        if self.cube:
            if self.cube_touch_button():
                self.reset_game()
        if self.laser:
            if self.robot_touch_laser():
                self.reset_game()

        screen.blit(background, (0, 0))
        if self.debug:
            space.debug_draw(draw_options)
        for obj in self.objects:
            obj.draw()
        space.step(0.02)

    def cube_touch_button(self):
        dPos = self.cube.body.position-self.button.center    
        if abs(dPos) < self.button.radius:
            return(True)
        return(False)
    
    def robot_touch_laser(self):
        dPos = self.robot.body.position-self.laser.center    
        if abs(dPos) < self.laser.radius:
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


    def random_pos(self):
        #Playable zone is x = 80-640; y = 122-384.
        in_zone_pos = lambda : (random.randint(100, 620),random.randint(140, 340))

        far_enought = False
        while(not far_enought):
            pos = in_zone_pos()
            far_enought = True
            for obj in self.objects:
                if abs(pos - obj.body.position) < 80:
                    far_enought = False
        return pos

    def reset_game(self):
        """Set player level."""
        self.remove_objects()
        self.set_ground()

        #self.button = Button((400,300))
        #self.cube = Cube((300,300))

        self.robot = Robot(self.random_pos())
        self.laser = Laser(self.random_pos())
        for i in range(8):
            self.obstacles.append(Obstacle(self.random_pos()))
