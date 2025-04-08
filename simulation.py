
"""
    Description

    Simulation setup for two robots

"""

import pygame
import sys
import pickle

# Constants
WIDTH, HEIGHT = 1000, 700
NODE_RADIUS = 4
ROBOT_RADIUS = 8
FPS = 60
SPEED = 2
GRID_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
LIGHT_GREY = (220, 220, 220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Simulation")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

# Modes
mode = "SHELF"

# Data storage
shelves = []
nodes = []
paths = []
robot_a = {'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': [], 'index': 0}
robot_b = {'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': [], 'index': 0}

placing_shelf = False
shelf_start = None

path_temp = []
robot_path_temp = []
current_robot_editing = None
robot_set_stage = 0

simulating = False

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GREY, (0, y), (WIDTH, y))

def draw():
    screen.fill(WHITE)
    draw_grid()

    # Draw shelves
    for rect in shelves:
        pygame.draw.rect(screen, GREY, rect)

    # Draw paths
    for start, end in paths:
        pygame.draw.line(screen, BLACK, start, end, 2)

    # Draw nodes
    for node in nodes:
        pygame.draw.circle(screen, BLUE, node, NODE_RADIUS)

    # Draw robot paths
    if len(robot_a['full_path']) > 1:
        pygame.draw.lines(screen, RED, False, robot_a['full_path'], 2)
    if len(robot_b['full_path']) > 1:
        pygame.draw.lines(screen, GREEN, False, robot_b['full_path'], 2)

    if robot_a['pos']:
        pygame.draw.circle(screen, RED, (int(robot_a['pos'][0]), int(robot_a['pos'][1])), ROBOT_RADIUS)
    if robot_b['pos']:
        pygame.draw.circle(screen, GREEN, (int(robot_b['pos'][0]), int(robot_b['pos'][1])), ROBOT_RADIUS)

    # Draw robot A start/goal
    if robot_a['start']:
        pygame.draw.circle(screen, RED, robot_a['start'], ROBOT_RADIUS, 2)
    if robot_a['goal']:
        pygame.draw.circle(screen, RED, robot_a['goal'], ROBOT_RADIUS, 2)

    # Draw robot B start/goal
    if robot_b['start']:
        pygame.draw.circle(screen, GREEN, robot_b['start'], ROBOT_RADIUS, 2)
    if robot_b['goal']:
        pygame.draw.circle(screen, GREEN, robot_b['goal'], ROBOT_RADIUS, 2)


    # Draw current mode
    mode_text = font.render(f"Mode: {mode}", True, BLACK)
    screen.blit(mode_text, (10, 10))

    pygame.display.flip()

def snap_to_grid(pos):
    x = round(pos[0] / GRID_SIZE) * GRID_SIZE
    y = round(pos[1] / GRID_SIZE) * GRID_SIZE
    return (x, y)

def get_nearest_node(pos):
    for node in nodes:
        if pygame.Rect(node[0] - 10, node[1] - 10, 20, 20).collidepoint(pos):
            return node
    return None

def move_robot(robot):
    if robot['index'] < len(robot['full_path']) - 1:
        current = pygame.Vector2(robot['pos'])
        target = pygame.Vector2(robot['full_path'][robot['index'] + 1])
        direction = (target - current)
        distance = direction.length()

        if distance != 0:
            direction = direction.normalize()
            step = direction * SPEED

            if distance <= SPEED:
                robot['pos'] = target
                robot['index'] += 1
            else:
                robot['pos'] = (current + step)
                
        # here if distance is less than threshold we can send request to server
                
def save_simulation():
    data = {
        'shelves': shelves,
        'nodes': nodes,
        'paths': paths,
        'robot_a': robot_a,
        'robot_b': robot_b
    }
    with open('simulation_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print("Simulation data saved.")
    

running = True
while running:
    clock.tick(FPS)

    if simulating:
        if len(robot_a['full_path']) > 1:
            move_robot(robot_a)
        if len(robot_b['full_path']) > 1:
            move_robot(robot_b)

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mode = "SHELF"
            elif event.key == pygame.K_n:
                mode = "NODE"
            elif event.key == pygame.K_p:
                mode = "PATH"
            elif event.key == pygame.K_r:
                mode = "ROBOT"
            elif event.key == pygame.K_a:
                mode = "ROBOT_PATH_A"
                current_robot_editing = robot_a
                robot_path_temp = []
            elif event.key == pygame.K_b:
                mode = "ROBOT_PATH_B"
                current_robot_editing = robot_b
                robot_path_temp = []
            elif event.key == pygame.K_RETURN:
                if current_robot_editing and len(robot_path_temp) > 1:
                    current_robot_editing['full_path'] = robot_path_temp[:]
                    current_robot_editing['start'] = robot_path_temp[0]
                    current_robot_editing['goal'] = robot_path_temp[-1]
                    current_robot_editing['pos'] = robot_path_temp[0]
                    current_robot_editing['path'] = robot_path_temp[:]
                    robot_path_temp = []
                    current_robot_editing = None
                    mode = "ROBOT"
            elif event.key == pygame.K_SPACE:
                simulating = True
                if robot_a['start']:
                    robot_a['pos'] = robot_a['start']
                    robot_a['path'] = robot_a['full_path'][:]
                if robot_b['start']:
                    robot_b['pos'] = robot_b['start']
                    robot_b['path'] = robot_b['full_path'][:]
                print("robot a path: ", robot_a['full_path'])
                print("robot b path: ", robot_b['full_path'])
            elif event.key == pygame.K_c:
                shelves.clear()
                nodes.clear()
                paths.clear()
                robot_a.update({'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': []})
                robot_b.update({'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': []})
                path_temp.clear()
                robot_path_temp.clear()
                simulating = False
                placing_shelf = False
                shelf_start = None
                print("Cleared all data and reset simulation.")
            elif event.key == pygame.K_v:
                save_simulation()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            raw_pos = pygame.mouse.get_pos()
            pos = snap_to_grid(raw_pos)

            if mode == "SHELF":
                if not placing_shelf:
                    shelf_start = pos
                    placing_shelf = True
                else:
                    rect = pygame.Rect(min(shelf_start[0], pos[0]), min(shelf_start[1], pos[1]),
                                       abs(shelf_start[0] - pos[0]), abs(shelf_start[1] - pos[1]))
                    shelves.append(rect)
                    placing_shelf = False

            elif mode == "NODE":
                nodes.append(pos)

            elif mode == "PATH":
                nearest = get_nearest_node(pos)
                if nearest:
                    path_temp.append(nearest)
                    if len(path_temp) == 2:
                        paths.append((path_temp[0], path_temp[1]))
                        path_temp = []
                            
            elif mode == "ROBOT":
                nearest = get_nearest_node(pos)
                if nearest:
                    if event.button == 1:  # Left click → Robot A
                        if robot_a['start'] is None:
                            robot_a['start'] = nearest
                            print("Robot A start set to", nearest)
                        elif robot_a['goal'] is None:
                            robot_a['goal'] = nearest
                            print("Robot A goal set to", nearest)
                    elif event.button == 3:  # Right click → Robot B
                        if robot_b['start'] is None:
                            robot_b['start'] = nearest
                            print("Robot B start set to", nearest)
                        elif robot_b['goal'] is None:
                            robot_b['goal'] = nearest
                            print("Robot B goal set to", nearest)

            elif mode in ["ROBOT_PATH_A", "ROBOT_PATH_B"]:
                nearest = get_nearest_node(pos)
                if nearest and nearest not in robot_path_temp:
                    robot_path_temp.append(nearest)
                    print("point added to path ", nearest)

pygame.quit()
sys.exit()
