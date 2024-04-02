import pygame
from pygame.locals import *

import pymunk
from pymunk.pygame_util import *
from pymunk import Vec2d
import math
import random

pymunk.pygame_util.positive_y_is_up = False
width, height = 100, 100
background = pygame.image.load('./sprites/capture.jpg')
clock = pygame.time.Clock()

pygame.init()
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

    #    self.body.velocity = self.body.velocity*0.80
    #    self.body.angular_velocity = self.body.angular_velocity*0.80

        pos = to_pygame(self.body.position, screen)
        rect = img.get_rect()
        rect.center = to_pygame(self.body.position, screen)
        screen.blit(img, rect)


class Button(Object):
    radius = 6
    img = pygame.image.load('./sprites/Button.png').convert_alpha()
    img = pygame.transform.scale(img, (radius*2, radius*2))
    def __init__(self, pos):
        super().__init__(pos) 
        self.center = pos+ Vec2d(self.radius/2,self.radius/2)

class  Laser(Object):
    radius = 5
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
    pic_size = (4, 4)
    img = pygame.image.load('./sprites/obstacle100.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)


class Cube(Rectangle):
    pic_size = (4, 4)
    img = pygame.image.load('./sprites/cube.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)


class Robot(Object):
    pic_size = (12, 8)
    img = pygame.image.load('./sprites/robot100.png').convert_alpha()
    img = pygame.transform.scale(img, pic_size)

    def __init__(self, pos):
        super().__init__(pos)
        self.speed = 4
        self.rotation_speed_right = 2*math.pi/15
        self.rotation_speed_left = 2*math.pi/16.5
        #Init shape
        size = self.img.get_size()
        #print(f"Robot size {size}")
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
        self.body.angular_velocity = self.rotation_speed_right  # Turn right

    def rotate_left(self):
        self.body.angular_velocity = -self.rotation_speed_left  # Turn left

    def stop(self):
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0



class Game:
    objects = []
    obstacles = []
    score = 0
    debug = False
    cube = 0
    laser = 0
    lose = False
    level = 'laser'
    n_obstacles = 0

    def __init__(self, level, obstacles_n):
        self.score = 0
        self.n_obstacles = obstacles_n
        if level == 'laser' or level == 'cube':
            self.level = level
        else:
            print("Wrong level name!")

        space.add_collision_handler(1, 2).begin = self.robot_hit_wall

    def robot_hit_wall(self,arbiter, space, _):
        self.lose = True
        return True

    def set_ground(self):
        top = pymunk.Segment(space.static_body, (5, 16), (100, 16), 3)
        left = pymunk.Segment(space.static_body, (2, 19), (0, 93), 3)
        bottom = pymunk.Segment(space.static_body, (2, 93), (100, 100), 3)
        right = pymunk.Segment(space.static_body, (100, 19), (100, 100), 3)
        walls = [top,left,bottom,right]
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
        screen.blit(background, (0, 0))
        if self.debug:
            space.debug_draw(draw_options)
        for obj in self.objects:
            obj.draw()
        

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
    
    def win_condition(self):
        if self.level == 'laser' and self.robot_touch_laser():
            return True
        
        if self.level == 'cube' and self.cube_touch_button():
            return True
        
        return False
    
    def do_event(self, event):

        if event == K_d:
            self.debug = not self.debug
            return
            
        if event == K_r:
            self.reset_game()
            return

        if event == K_SPACE:
            self.robot.stop()
            return 
            
        if event == K_UP:
            self.robot.stop()
            self.robot.forward()
            return
            
        if event == K_RIGHT:
            self.robot.stop()
            self.robot.rotate_right()
            return
            
        if event == K_LEFT:
            self.robot.stop()
            self.robot.rotate_left()
            return

    def random_pos(self):
        #Playable zone is x = 80-640; y = 122-384.
        in_zone_pos = lambda : (random.randint(15, 90),random.randint(30, 80))

        far_enought = False
        i=0
        while(not far_enought):
            i+=1
            if i > 10000:
                print('Can\'t place all objects')
                break

            pos = in_zone_pos()
            far_enought = True
            for obj in self.objects:
                if abs(pos - obj.body.position) < 10:
                    far_enought = False
        return pos

    def reset_game(self):
        """Set player level."""
        self.lose = False
        self.remove_objects()
        self.set_ground()

        if self.level == 'laser':
            self.robot = Robot(self.random_pos())
            self.laser = Laser(self.random_pos())

        if self.level == 'debug':
            self.robot = Robot((320,280))
            self.laser = Laser((320,200))
            self.obstacles.append(Obstacle((320,240)))
            self.debug = True

        if self.level == 'cube':
            self.robot = Robot(self.random_pos())
            self.button = Button(self.random_pos())
            self.cube = Cube(self.random_pos())

        self.robot.body.angle = random.random()*math.pi*2

        for i in range(self.n_obstacles):
            self.obstacles.append(Obstacle(self.random_pos()))
