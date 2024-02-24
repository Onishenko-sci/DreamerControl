import pygame as py
import sys
import math

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



# Initialize py
py.init()

# Set up the screen
width, height = 1024, 768
screen = py.display.set_mode((width, height))
py.display.set_caption("Move the Robot")

obstacle = py.Surface((50,50))
obstacle.fill('red')
obstacle_pos = (100,100)
obstacle_mask = py.mask.from_surface(obstacle)

# Load the background image
background = py.image.load('./game/capture.jpg')  # Replace 'your_image.jpg' with the actual filename

robot = Robot()

# Main game loop
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

    # Get the keys currently held down
    keys = py.key.get_pressed()

    # Continuous movement
    if keys[py.K_LEFT]:
        robot.rotate_left()  # Turn left
    if keys[py.K_RIGHT]:
        robot.rotate_right()  # Turn right
    if keys[py.K_UP]:
        robot.forward()
    if keys[py.K_DOWN]:
        robot.backward()

    # Fill the background
    screen.blit(background, (0, 0))

    robot.update()

    if py.mouse.get_pos():
        obstacle_pos = py.mouse.get_pos()

    screen.blit(obstacle,obstacle_pos)
    if robot.mask.overlap(obstacle_mask, (obstacle_pos[0]- robot.rect.left, obstacle_pos[1]- robot.rect.top)):
        print("Collision")



    # Update the display
    py.display.flip()

    # Control the frame rate
    py.time.Clock().tick(60)
