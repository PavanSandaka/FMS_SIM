import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
ROBOT_RADIUS = 8
FPS = 5

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Simulation")
clock = pygame.time.Clock()

# Define grid points
grid_points = []
for x in range(0, WIDTH, GRID_SIZE):
    for y in range(0, HEIGHT, GRID_SIZE):
        grid_points.append((x, y))

# Define shelves (sample: list of rects)
shelves = [
    pygame.Rect(80, 40, 40, 120),
    pygame.Rect(80, 200, 40, 120),
    pygame.Rect(240, 40, 40, 120),
    pygame.Rect(240, 200, 40, 120),
    pygame.Rect(400, 40, 40, 280),
    pygame.Rect(560, 40, 40, 120),
    pygame.Rect(560, 200, 40, 120)
]

# Define Robot A and B paths (as list of grid coordinates)
robot_a_path = [(0, 40), (80, 40), (80, 440), (400, 440)]
robot_b_path = [(720, 280), (400, 280), (400, 120), (240, 120)]

# Initial positions
robot_a_index = 0
robot_b_index = 0

def draw():
    screen.fill(WHITE)

    # Draw grid points
    for point in grid_points:
        pygame.draw.circle(screen, BLUE, point, 3)

    # Draw shelves
    for shelf in shelves:
        pygame.draw.rect(screen, GRAY, shelf)

    # Draw robot paths
    pygame.draw.lines(screen, RED, False, robot_a_path, 3)
    pygame.draw.lines(screen, GREEN, False, robot_b_path, 3)

    # Draw robots
    if robot_a_index < len(robot_a_path):
        pygame.draw.circle(screen, RED, robot_a_path[robot_a_index], ROBOT_RADIUS)

    if robot_b_index < len(robot_b_path):
        pygame.draw.circle(screen, GREEN, robot_b_path[robot_b_index], ROBOT_RADIUS)

    pygame.display.flip()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    # Move robots step by step
    if robot_a_index < len(robot_a_path) - 1:
        robot_a_index += 1

    if robot_b_index < len(robot_b_path) - 1:
        robot_b_index += 1

    clock.tick(FPS)
