import pygame as py
import sys
import math

import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

class Robot():
    def __init__(self):
        super().__init__()
        self.image = py.image.load('./game/car.png')
        self.original = py.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        self.mask = py.mask.from_surface(self.image)
        self.size = self.rect.size
        self.speed = 10
        self.rotation_angle = 0  # Initial angle of the robot
        self.rotation_speed = 5  # Initial angle of the robot

        self.rect_color = (255, 0, 0)  # Red
        self.rect_thickness = 2

        #Phisics
        self.mass = 1
        self.moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = (width // 2, height // 2)
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = 0.8
        self.shape.friction = 1
        self.shape.color = (255,255,255,255)
        space.add(self.body,self.shape)

    def update(self):
        self.image = py.transform.rotate(self.original, self.rotation_angle)
        #Update this only when you in danger zone (Rectnangles collision)
        #self.mask = py.mask.from_surface(self.image)

        if self.rotation_angle == 360 or self.rotation_angle ==-360:
            self.rotation_angle = 0
        # Get a new rectangle with the rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

        screen.blit(self.image, self.rect)
        py.draw.rect(screen, self.rect_color, self.rect, self.rect_thickness)

    def forward(self):
        # Calculate the movement vector based on the current rotation angle
        move_x = math.cos(math.radians(self.rotation_angle)) * self.speed
        move_y = math.sin(math.radians(self.rotation_angle)) * self.speed
        # Move the robot
        self.rect.x += move_x
        self.rect.y -= move_y
    
    def backward(self):
        # Calculate the movement vector based on the current rotation angle (backward)
        move_x = math.cos(math.radians(self.rotation_angle + 180)) * self.speed
        move_y = math.sin(math.radians(self.rotation_angle + 180)) * self.speed
        # Move the robot
        self.rect.x += move_x
        self.rect.y -= move_y
    
    def rotate_right(self):
        self.rotation_angle -= self.rotation_speed  # Turn right

    def rotate_left(self):
        self.rotation_angle += self.rotation_speed  # Turn left

class Cube():
    def __init__(self):
        super().__init__()
        self.image = py.image.load('./game/Cube.png')
        self.original = py.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        self.mask = py.mask.from_surface(self.image)
        self.size = self.rect.size

# Initialize py
py.init()

# Set up the screen
width, height = 1024, 768
FPS = 60
screen = py.display.set_mode((width, height))
py.display.set_caption("Move the Robot")

clock = py.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()
space.gravity = 0, 10 

#платформа
segment_shape = pymunk.Segment(space.static_body, (1, height), (width, height), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.4
segment_shape.friction = 1.0

#Cube
square_mass, square_size = 1, (60, 60)
square_moment = pymunk.moment_for_box(square_mass, square_size)
square_body = pymunk.Body(square_mass, square_moment)
square_body.position = (100,100)
square_shape = pymunk.Poly.create_box(square_body, square_size)
square_shape.elasticity = 0.8
square_shape.friction = 1.0
square_shape.color = (255,255,255,255)
space.add(square_body, square_shape)

# Load the background image
background = py.image.load('./game/capture.jpg')  # Replace 'your_image.jpg' with the actual filename

robot = Robot()

# Main game loop
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

    # Recieve game inputs
    keys = py.key.get_pressed()

    if keys[py.K_LEFT]:
        robot.rotate_left() 
    if keys[py.K_RIGHT]:
        robot.rotate_right() 
    if keys[py.K_UP]:
        robot.forward()
    if keys[py.K_DOWN]:
        robot.backward()

    # Drow objects on screen
    screen.blit(background, (0, 0))

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    robot.update()

    py.display.flip()
    # Control the frame rate
    clock.tick(FPS)
