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

## Controls

- **s**: Switch to Shelf Placement mode
- **n**: Switch to Node Placement mode
- **1-9**: Select robot to define path (press Enter when done)
- **Space**: Start simulation
- **r**: Restart simulation (reset robot positions)
- **c**: Clear all data
- **v**: Save simulation data
- **l**: Load simulation data

## Mouse Controls

- **Left Click**: Place shelves, nodes, or select path nodes depending on current mode

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
   python simulation.py
   ```

## How It Works

1. Place shelves to create obstacles
2. Place nodes to define possible robot paths
3. Select robots (keys 1-9) and create paths
4. Press Space to start the simulation
5. Use r to reset or c to clear

## Project Structure

- `simulation.py`: Main simulation logic
- `utils/base_robot.py`: Robot class definition
- `utils/conflict_handler.py`: Conflict detection and resolution logic

## TODO

- Resolve the bug in simulation, the robot is getting stuck when it has to go to the top left corner node.
- Reroute the robot if two robots are stuck for same conflict.

## Next Steps

- Test it thoroughly in different cases.
- Add load button and dynamic buttons to change battery level and priority level in GUI
- Implement more advanced conflict resolution strategies
- Add statistics tracking
- Support for larger maps and more robots