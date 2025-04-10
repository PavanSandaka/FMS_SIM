# Robot Simulation

A graphical simulation for multi-robot coordination with conflict resolution.

## Description

This project simulates multiple robots navigating through a warehouse environment with shelves and nodes. The simulation implements conflict detection and resolution strategies to handle situations where robots might compete for the same path.

## Features

- Interactive grid-based environment
- Place shelves and nodes to create layouts
- Define custom paths for each robot
- Conflict detection and resolution for robot coordination
- Real-time simulation with adjustable parameters
- Save and load simulation configurations
- Automated simulation mode with random path generation

## Simulation Modes

### Interactive Simulation (`simulation.py`)

The standard simulation allows you to manually create the environment and robot paths.

#### Controls
- **s**: Switch to Shelf Placement mode
- **n**: Switch to Node Placement mode
- **1-9**: Select robot to define path (press Enter when done)
- **Space**: Start simulation
- **r**: Restart simulation (reset robot positions)
- **c**: Clear all data
- **v**: Save simulation data
- **l**: Load simulation data

#### Mouse Controls
- **Left Click**: Place shelves, nodes, or select path nodes depending on current mode

### Automated Simulation (`automated_simulation.py`)

The automated simulation generates random paths for robots and handles conflicts automatically.

#### Controls
- **Space**: Pause/Resume simulation
- **r**: Reset simulation (generate new random paths)

#### Setup
When running the automated simulation, you'll be prompted to enter:
1. Number of robots
2. Number of columns in the grid
3. Number of rows in the grid

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. Run the simulation:
   ```
   # For interactive simulation
   python simulation.py
   
   # For automated simulation
   python automated_simulation.py
   ```

## How It Works

### Interactive Simulation
1. Enter number of robots for the simulation
2. Place shelves to create obstacles (optional)
3. Place nodes to define possible robot paths
4. Select robots (keys 1-9) and create paths
5. Press Space to start the simulation
6. Use r to reset or c to clear

### Automated Simulation
1. Enter the number of robots and grid dimensions
2. The simulation creates a grid of nodes and assigns random start positions
3. Each robot is given a random priority and battery level
4. Robots automatically navigate to random goals
5. When a robot reaches its goal, it gets a new random goal
6. Conflict detection prevents robots from colliding

## Project Structure

- `simulation.py`: Main interactive simulation logic
- `automated_simulation.py`: Automated simulation with random path generation
- `utils/base_robot.py`: Robot class definition
- `utils/conflict_handler.py`: Conflict detection and resolution logic

## TODO

- Resolve the bug in simulation where robots get stuck when heading to the top left corner node
- Reroute robots if two robots remain stuck in the same conflict
- Add dynamic battery consumption based on robot movement
- Implement different conflict resolution strategies based on priority levels

## Next Steps

- Test thoroughly in different cases
- Add load button and dynamic buttons to change battery level and priority level in GUI
- Implement more advanced conflict resolution strategies
- Add statistics tracking
- Support for larger maps and more robots
- Add visualization for conflict events
