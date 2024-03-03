import requests
import pygame

# Set up Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 300))

# Dictionary to map keys to endpoints 
key_to_endpoint = {
    pygame.K_SPACE: "/stop" ,    
    pygame.K_UP: "/forward",
    pygame.K_RIGHT: "/right",
    pygame.K_LEFT: "/left",
    pygame.K_DOWN: "/backward"
}

def push_button(endpoint):
    url = "http://192.168.1.145"
    full_url = url + endpoint
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
    push_button("")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in key_to_endpoint:
                    push_button(key_to_endpoint[event.key])

    
    pygame.quit()

if __name__ == "__main__":
    main()
