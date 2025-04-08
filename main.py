from utils.base_robot import Robot
import time

def get_common_path(path1, path2):
    return list(set(path1) & set(path2))

def find_conflicts(robot, robots):
    conflicts = []
    
    # Check for conflict with the current robot with all the other robots
    for other_robot in robots:
        # Skip comparing the robot with itself
        if other_robot.name == robot.name:
            continue
        
        # Find common points in their paths
        common_points = get_common_path(robot.path, other_robot.path)
        
        if common_points:
            conflicts.append({
                "robot": other_robot.name,
                "common_points": common_points
            })
    
    return conflicts

def handle_conflicts(conflict, robot):
    
    # this function tells if the robot needs to go forward or wait
    # now here check the priority for the aisle, score both the robots and decide which should be given priority
    
    # Priority Scoring Criteria:
    # Proximity to Conflict Point
    # Robot closer to the conflict point receives higher priority
    # Reduces overall system waiting time

    # Task Priority/Deadline
    # Robots carrying time-sensitive items receive higher priority
    # Ensures critical deliveries meet their deadlines

    # Battery Level Consideration
    # Lower battery level robots get priority
    # Factors in load weight impact on power consumption
    # Prevents robots from depleting their battery before task completion

    # Distance to Goal
    # Robots farther from their destination receive higher priority
    # Prevents cascading delays in subsequent operations

    # Cargo Volume/Complexity
    # Robots carrying more items or requiring complex unloading procedures get priority
    # Optimizes downstream handling operations

    pass


robots = [
    Robot(name="R1", path=[1, 2, 3, 4, 5, 12, 15, 16, 17, 18, 19], priority=2, battery_lvl=50),
    Robot(name="R2", path=[10, 11, 12, 5, 4, 3, 6, 7], priority=1, battery_lvl=25),
    # Robot(name="R3", path=[1, 5, 6], priority=3),
]


print(find_conflicts(robots[1], robots))



"""
Algorithm

1. find the conflicts
    If no conflicts good, go to next
    If there are conflicts check with what all robots if has conflicts

2. Check if the conflict is a common aisle or just a node
    if its an aisle, how for away is it from the aisle

"""