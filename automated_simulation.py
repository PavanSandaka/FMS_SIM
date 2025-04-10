import time
import pygame
import sys
import random
import heapq
from utils.base_robot import Robot
from utils.conflict_handler import ConflictDetector, ConflictResolver, Decision

# Constants
WIDTH, HEIGHT = 1000, 700
NODE_RADIUS = 4
ROBOT_RADIUS = 8
FPS = 60
SPEED = 1
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
pygame.display.set_caption("Automated Robot Simulation")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

# Function to generate grid nodes
def generate_grid_nodes(cols=10, rows=10):
    nodes = {}
    node_id = 0
    
    # Calculate spacing to fit grid within screen dimensions
    # Leave some margin around the edges
    margin = 50
    available_width = WIDTH - (2 * margin)
    available_height = HEIGHT - (2 * margin)
    
    # Calculate spacing between nodes
    x_spacing = available_width / (cols - 1) if cols > 1 else available_width
    y_spacing = available_height / (rows - 1) if rows > 1 else available_height
    
    # Start positions - centered in screen
    start_x = margin
    start_y = margin
    
    for y in range(rows):
        for x in range(cols):
            nodes[node_id] = (start_x + x * x_spacing, start_y + y * y_spacing)
            node_id += 1
            
    return nodes

# Function to generate edges between nodes
def generate_edges(nodes, cols=10, rows=10):
    edges = {}
    
    for node_id in nodes:
        edges[node_id] = []
        
        # Check right neighbor
        if (node_id + 1) % cols != 0 and node_id + 1 < len(nodes):
            edges[node_id].append(node_id + 1)
            
        # Check left neighbor
        if node_id % cols != 0 and node_id - 1 >= 0:
            edges[node_id].append(node_id - 1)
            
        # Check down neighbor
        if node_id + cols < len(nodes):
            edges[node_id].append(node_id + cols)
            
        # Check up neighbor
        if node_id - cols >= 0:
            edges[node_id].append(node_id - cols)
            
    return edges

# Dijkstra's algorithm for path planning
def find_path(start, goal, edges):
    if start == goal:
        return [start]
        
    open_set = [(0, start)]
    closed_set = set()
    g_score = {start: 0}
    came_from = {}
    
    while open_set:
        current_g, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # Reverse path
            
        closed_set.add(current)
        
        for neighbor in edges[current]:
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + 1  # Cost is 1 for grid movement
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g  # No heuristic, so f = g
                
                # Check if in open set
                in_open_set = False
                for i, (_, node) in enumerate(open_set):
                    if node == neighbor:
                        in_open_set = True
                        break
                        
                if not in_open_set:
                    heapq.heappush(open_set, (f_score, neighbor))
                    
    return []  # No path found

# Generate random goal for a robot
def generate_random_goal(robot, nodes, edges, occupied_nodes):
    available_nodes = list(set(nodes.keys()) - set(occupied_nodes))
    
    if not available_nodes:
        return False
        
    goal_node = random.choice(available_nodes)
    
    # Find path from current node to goal
    if robot.current_node is not None:
        path = find_path(robot.current_node, goal_node, edges)
        if path:
            robot.handle_path(path)
            return True
            
    return False

# Draw functions
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GREY, (0, y), (WIDTH, y))

def draw():
    screen.fill(WHITE)
    # draw_grid()

    # Draw nodes and edges
    for node_id, pos in nodes.items():
        pygame.draw.circle(screen, BLUE, pos, NODE_RADIUS)
        
    # Draw edges
    for node_id, neighbors in edges.items():
        for neighbor in neighbors:
            pygame.draw.line(screen, LIGHT_GREY, nodes[node_id], nodes[neighbor], 1)

    # Draw robots and their paths
    for i, robot in enumerate(robots):
        color = ROBOT_COLORS[i % len(ROBOT_COLORS)]
        
        # Draw robot paths
        if robot.full_path and len(robot.full_path) >= 2:
            path_points = [nodes[node_id] for node_id in robot.full_path]
            
            if len(path_points) >= 2:
                pygame.draw.lines(screen, color, False, path_points, 2)
            
                # Highlight start and goal
                pygame.draw.circle(screen, color, path_points[0], NODE_RADIUS + 2, 2)
                pygame.draw.circle(screen, color, path_points[-1], NODE_RADIUS + 2, 2)

        # Draw the robot itself
        if robot.current_pose:
            pygame.draw.circle(screen, color, (int(robot.current_pose[0]), int(robot.current_pose[1])), ROBOT_RADIUS)
            robot_text = font.render(f"{robot.name} {'' if not robot.waiting else '(W)'}", True, BLACK)
            screen.blit(robot_text, (int(robot.current_pose[0]) - 15, int(robot.current_pose[1]) - 25))

    # Display simulation stats
    stats_text = font.render(f"Robots: {len(robots)} | Simulation Running", True, BLACK)
    screen.blit(stats_text, (10, 10))

    pygame.display.flip()

def move_robot(robot):
    if not robot.next_node or robot.waiting:
        return
        
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


def make_decision(current_robot, robots):
    # Find conflicts and make decision
    conflicts = conflict_detector.find_conflicts(current_robot, robots)
    decision = conflict_resolver.handle_conflicts(conflicts, current_robot)
    
    return decision

# Set up simulation parameters
num_robots = int(input("Enter the number of robots: "))
grid_cols = int(input("Enter number of columns in grid (default 10): ") or "10")
grid_rows = int(input("Enter number of rows in grid (default 10): ") or "10")

# Generate grid nodes and edges
nodes = generate_grid_nodes(cols=grid_cols, rows=grid_rows)
edges = generate_edges(nodes, cols=grid_cols, rows=grid_rows)

# Create robots
robots = [Robot(name=f"R{i+1}") for i in range(num_robots)]

# Set initial priorities and battery levels
for i, robot in enumerate(robots):
    robot.update_priority(random.randint(1, 10))
    robot.update_battery_level(random.randint(50, 100))
    
    # Assign random starting position
    start_node = random.choice(list(nodes.keys()))
    robot.current_node = start_node
    robot.current_pose = nodes[start_node]
    
    # Generate initial random goal
    occupied_nodes = [r.current_node for r in robots[:i]]
    generate_random_goal(robot, nodes, edges, occupied_nodes)

# Create conflict handler
conflict_detector = ConflictDetector()
conflict_resolver = ConflictResolver()

# Main simulation loop
running = True
simulating = True
last_goal_update = pygame.time.get_ticks()
goal_update_interval = 500  # Check for new goals every 500ms

while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
            elif event.key == pygame.K_r:
                # Reset simulation
                for robot in robots:
                    robot.reset_robot()
                    start_node = random.choice(list(nodes.keys()))
                    robot.current_node = start_node
                    robot.current_pose = nodes[start_node]
                    generate_random_goal(robot, nodes, edges, [])

    if simulating:
        # Update robots
        for i, robot in enumerate(robots):
            
            if robot.current_pose == nodes[robot.full_path[-1]]:
                occupied_nodes = [r.current_node for r in robots if r != robot]
                generate_random_goal(robot, nodes, edges, occupied_nodes)
                
            if robot.current_pose == nodes[robot.current_node]:
                decision = make_decision(robot, robots)
                if decision != Decision.FORWARD.value:
                    robot.waiting = True
                    continue
                robot.waiting = False
                
            move_robot(robot)
    
    try:
        draw()
    except Exception as e:
        print(f"Error in draw: {e}")
        time.sleep(1)

pygame.quit()
sys.exit()
