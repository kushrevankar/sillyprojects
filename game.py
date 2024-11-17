import pygame
import sys
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("simple game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#fps
clock = pygame.time.Clock()
FPS = 240

#player setup
player_pos = np.array([400, 300])
player_size = 20
player_speed = 5

#obstacle setup
obstacle_pos = np.array([100, 100])
obstacle_velocity = np.array([2, 3])
obstacle_size = 20

#logic
def game_loop():
    global player_pos, obstacle_pos, obstacle_velocity
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #player movement
        keys = pygame.key.get_pressed()
        movement = np.array([0, 0])
        if keys[pygame.K_LEFT]:
            movement += np.array([-1, 0])
        if keys[pygame.K_RIGHT]:
            movement += np.array([1, 0])
        if keys[pygame.K_UP]:
            movement += np.array([0, -1])
        if keys[pygame.K_DOWN]:
            movement += np.array([0, 1])

        #add diagonal movement
        if np.linalg.norm(movement) != 0:
            movement = movement / np.linalg.norm(movement)

        #player position rules
        player_pos += (movement * player_speed).astype(int)

        #boundary constraints
        player_pos[0] = np.clip(player_pos[0], player_size // 2, WIDTH - player_size // 2)
        player_pos[1] = np.clip(player_pos[1], player_size // 2, HEIGHT - player_size // 2)

        #obstacle position
        obstacle_pos += obstacle_velocity

        #reverse obstacle direction on boundary collision
        if obstacle_pos[0] < 0 or obstacle_pos[0] > WIDTH - obstacle_size:
            obstacle_velocity[0] *= -1
        if obstacle_pos[1] < 0 or obstacle_pos[1] > HEIGHT - obstacle_size:
            obstacle_velocity[1] *= -1
        
        #check for collisions
        distance = np.linalg.norm(player_pos - obstacle_pos)
        if distance < (player_size // 2 + obstacle_size // 2):
            print("Game Over!")
            pygame.quit()
            sys.exit()

        #render
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (*player_pos - player_size // 2, player_size, player_size))
        pygame.draw.rect(screen, RED, (*obstacle_pos - obstacle_size // 2, obstacle_size, obstacle_size))

        #update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()