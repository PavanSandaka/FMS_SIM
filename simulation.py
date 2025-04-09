
"""
    Description

    Simulation setup

"""

import pygame
import sys
import pickle
from utils.base_robot import Robot
from utils.conflict_handler import ConflictDetector, ConflictResolver, Decision

# Constants
WIDTH, HEIGHT = 1000, 700
NODE_RADIUS = 4
ROBOT_RADIUS = 8
FPS = 60
SPEED = 2
GRID_SIZE = 40

ROBOT_COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 165, 0),    # Orange
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (128, 0, 128),    # Purple
    (128, 128, 0),    # Olive
    (0, 128, 128)     # Teal
]

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
nodes = {}   # {1: (x, y), 2: (x, y), ...}
# robot_a = {'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': [], 'index': 0}
# robot_b = {'start': None, 'goal': None, 'path': [], 'pos': None, 'full_path': [], 'index': 0}
robot_a = Robot(name="R1")
robot_b = Robot(name="R2")

robots = [robot_a, robot_b]

node_counter = 1      # Auto-increment node name

placing_shelf = False
shelf_start = None

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

    # Draw nodes
    for node, node_pose in nodes.items():
        pygame.draw.circle(screen, BLUE, node_pose, NODE_RADIUS)

    for i, robot in enumerate(robots):
        color = robot_colors[i]
        
        # Draw robot paths
        if robot.full_path:
            path_points = [nodes[i] for i in robot.full_path]
            
            pygame.draw.lines(screen, color, False, path_points, 2)
            
            pygame.draw.circle(screen, color, path_points[0], ROBOT_RADIUS, 2)
            pygame.draw.circle(screen, color, path_points[-1], ROBOT_RADIUS, 2)


        if robot.current_pose:
            pygame.draw.circle(screen, color, (int(robot.current_pose[0]), int(robot.current_pose[1])), ROBOT_RADIUS)


    # Draw current mode
    mode_text = font.render(f"Mode: {mode}", True, BLACK)
    screen.blit(mode_text, (10, 10))

    pygame.display.flip()

def snap_to_grid(pos):
    x = round(pos[0] / GRID_SIZE) * GRID_SIZE
    y = round(pos[1] / GRID_SIZE) * GRID_SIZE
    return (x, y)


def get_nearest_node(pos):
    for node_id, node_pos in nodes.items():
        if pygame.Rect(node_pos[0] - 10, node_pos[1] - 10, 20, 20).collidepoint(pos):
            return node_id
    return None

def make_decision(current_robot, robots):
    # Find conflicts and make decision
    conflicts = conflict_detector.find_conflicts(current_robot, robots)
    decision = conflict_resolver.handle_conflicts(conflicts, current_robot)
        
    return decision
    

def move_robot(robot):
    current = pygame.Vector2(robot.current_pose)
    target = pygame.Vector2(nodes[robot.next_node])
    direction = (target - current)
    distance = direction.length()

    if distance != 0:
        direction = direction.normalize()
        step = direction * SPEED

        if distance <= SPEED:
            robot.move_forward()    
            robot.current_pose = nodes[robot.current_node]            
        else:
            robot.current_pose = (current + step)
                
                
def save_simulation():
    data = {
        'shelves': shelves,
        'nodes': nodes,
        'robots': robots
    }
    with open('simulation_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print("Simulation data saved.")
    
priority_array = [5, 6]
battery_lvl_array = [50, 50]

num_robots = int(input("Enter the number of robots: "))
robots = [Robot(name=f"R{i+1}") for i in range(num_robots)]
robot_colors = {i: ROBOT_COLORS[i % len(ROBOT_COLORS)] for i in range(len(robots))}

for i, robot in enumerate(robots):
    robot.update_priority(priority_array[i])
    robot.update_battery_level(battery_lvl_array[i])
    
conflict_detector = ConflictDetector()
conflict_resolver = ConflictResolver()

running = True
while running:
    clock.tick(FPS)

    if simulating:            
        for robot in robots:
            if robot.next_node:
                # first make decision and based on that move the robot
                if robot.current_pose == nodes[robot.current_node]:
                    decision = make_decision(robot, robots)
                    if decision != Decision.FORWARD.value:
                        robot.waiting = True
                        continue
                    
                move_robot(robot)
                robot.waiting = False

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mode = "SHELF"
            elif event.key == pygame.K_n:
                mode = "NODE"
            elif event.key == pygame.K_RETURN:
                if current_robot_editing and len(robot_path_temp) > 1:
                    current_robot_editing.handle_path(robot_path_temp)
                    current_robot_editing.current_pose = nodes[robot_path_temp[0]]
                    robot_path_temp = []
                    current_robot_editing = None
                    mode = "SHELF"
            elif event.key == pygame.K_SPACE:
                simulating = True
            elif event.key == pygame.K_c:
                shelves.clear()
                nodes.clear()
                for robot in robots:
                    robot.reset_robot()

                robot_path_temp.clear()
                simulating = False
                placing_shelf = False
                shelf_start = None
                print("Cleared all data and reset simulation.")
            elif event.key == pygame.K_v:
                save_simulation()
            elif event.key == pygame.K_r:
                # Reset simulation without clearing data
                simulating = False
        
                # Reset all robots to their starting positions
                for robot in robots:
                    if robot.full_path:
                        robot.current_node = robot.full_path[0]
                        if len(robot.full_path) > 1:
                            robot.next_node = robot.full_path[1]
                        else:
                            robot.next_node = None
                        robot.current_pose = nodes[robot.current_node]
                        robot.waiting = False
                        robot.remaining_path = robot.full_path.copy()
        
                print("Simulation restarted - robots reset to starting positions.")
            elif pygame.K_1 <= event.key <= pygame.K_9:
                robot_index = event.key - pygame.K_1
                if robot_index < len(robots):
                    current_robot_editing = robots[robot_index]
                    mode = f"ROBOT_PATH_{robot_index + 1}"
                    robot_path_temp = []

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
                nodes[node_counter] = pos
                node_counter+=1

            elif "ROBOT_PATH" in mode:
                nearest = get_nearest_node(pos)
                if nearest and nearest not in robot_path_temp:
                    robot_path_temp.append(nearest)
                    # print("point added to path ", nearest)

pygame.quit()
sys.exit()
