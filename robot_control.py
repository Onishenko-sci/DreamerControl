import requests
import pygame

import cv2
import numpy as np
import requests
from io import BytesIO

# Set up Pygame
pygame.init()

screen_size = (240,240)
# Set up the screen
screen = pygame.display.set_mode(screen_size)

# Dictionary to map keys to endpoints 
key_to_endpoint = {
    pygame.K_SPACE: "/stop" ,    
    pygame.K_UP: "/forward",
    pygame.K_RIGHT: "/right",
    pygame.K_LEFT: "/left",
    pygame.K_DOWN: "/backward"
}

camera_url = "http://192.168.1.185"
cap = cv2.VideoCapture(camera_url + ":81/stream")
robot_url = "http://192.168.1.124"


def get_capture():
    # Get image from camera
    if cap.isOpened():
        ret, capture = cap.read()
        if ret:
            gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
            #gray = cv2.equalizeHist(gray)

    # Get the dimensions of the image
    h, w = capture.shape[:2]
    # Set camera parameters
    ''' 
    #For 640x480
    K = np.array([[574.85, 0, 298.35], [0, 559.21, 275.61], [0, 0, 1]])  # Intrinsic matrix
    D = np.array([-0.8, 1.2, -0.02, 0.036, -1.678])  # Distortion coefficients

    #For 240x240
    '''
    K = np.array([[254.85, 0, 119.60], [0, 247.14, 155.82], [0, 0, 1]])  # Intrinsic matrix
    D = np.array([-0.63, 0.57, -0.046, -0.0058, -0.483])  # Distortion coefficients
    # For 96x96
    #K = np.array([[111.73, 0, 48.25], [0, 109.6, 54.15], [0, 0, 1]])  # Intrinsic matrix
    #D = np.array([-0.8, 1.56, -0.0015, 0.0008, -2.72])  # Distortion coefficients

    # Perform lens distortion correction
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
    undistorted_capture = cv2.undistort(gray, K, D, None, new_camera_matrix)
    #Crop [112,47] [205,129]
    undistorted_capture = undistorted_capture[30:130,109:209]
    print(undistorted_capture.shape)

    undistorted_capture = cv2.resize(undistorted_capture, screen_size)


    #Translate it into pygame surfce
    capture_rgb = cv2.cvtColor(undistorted_capture, cv2.COLOR_BGR2RGB)
    capture_pygame = pygame.image.frombuffer(capture_rgb.flatten(), screen_size, 'RGB')
    return capture_pygame

def push_button(endpoint):
    full_url = robot_url + endpoint
    print(full_url)
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            print("Button " + endpoint + " pushed successfully")
        else:
            print("Failed to push button")
    except Exception as e:
        print("An error occurred:", e)


def main():
    running = True
    #set_resolution(camera_url, 8)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    #push_button("")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in key_to_endpoint:
                    #push_button(key_to_endpoint[event.key])
                    a=5
        
        #Render background
        background = get_capture()
        screen.blit(background, (0, 0))

        # Get the current FPS
        fps = clock.get_fps()
        # Render the FPS text
        fps_text = font.render(f"FPS is:  {fps}", True, (255, 0, 0))
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        clock.tick(50)

    
    pygame.quit()

if __name__ == "__main__":
    main()
