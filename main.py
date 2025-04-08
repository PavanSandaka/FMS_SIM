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
                "common_points": common_points,
                "robot_obj": other_robot  # Adding the actual robot object for detailed analysis
            })
    
    return conflicts

def find_entry_point_to_aisle(robot, aisle_points):
    # Find the first point in the robot's path that's part of the aisle
    entry_index = float('inf')
    entry_point = None
        
    for point in aisle_points:
        try:
            index = robot.path.index(point)
            if index < entry_index:
                entry_index = index
                entry_point = point
        except ValueError:
            continue
        
    return entry_index, entry_point

def handle_conflicts(conflicts, robot):
    if not conflicts:
        return "FORWARD"  # No conflicts, robot can proceed
        
    aisle_decisions = []
        
    for conflict in conflicts:
        other_robot_name = conflict["robot"]
        other_robot = conflict["robot_obj"]
        common_points = conflict["common_points"]
            
        # Consider the common points as a single aisle
        # Find entry points to the aisle for both robots
        robot_entry_index, robot_entry_point = find_entry_point_to_aisle(robot, common_points)
        other_entry_index, other_entry_point = find_entry_point_to_aisle(other_robot, common_points)
            
        # Calculate scores based on the entire aisle, not individual points
            
        # 1. Proximity to aisle entry (lower is better)
        robot_proximity = robot_entry_index
        other_proximity = other_entry_index
            
        # 2. Task priority (higher is better)
        robot_priority = robot.task_priority
        other_priority = other_robot.task_priority
            
        # 3. Battery level (lower is better - needs to reach charger)
        robot_battery = robot.battery_lvl
        other_battery = other_robot.battery_lvl
            
        # 4. Distance to goal (higher is better)
        robot_distance_to_goal = len(robot.path) - robot_proximity if robot_proximity != float('inf') else 0
        other_distance_to_goal = len(other_robot.path) - other_proximity if other_proximity != float('inf') else 0
            
        # Weights for different factors
        proximity_weight = 0.4
        priority_weight = 0.3
        battery_weight = 0.2
        distance_weight = 0.1
            
        # Convert proximity to a score where lower is better
        robot_proximity_score = 1/(robot_proximity+1) if robot_proximity != float('inf') else 0
        other_proximity_score = 1/(other_proximity+1) if other_proximity != float('inf') else 0
            
        # Battery score - lower battery means higher score
        robot_battery_score = (100 - robot_battery) / 100
        other_battery_score = (100 - other_battery) / 100
            
        # Calculate composite scores for the entire aisle
        robot_score = (robot_proximity_score * proximity_weight) + \
                    (robot_priority * priority_weight) + \
                    (robot_battery_score * battery_weight) + \
                    (robot_distance_to_goal * distance_weight)
                        
        other_score = (other_proximity_score * proximity_weight) + \
                    (other_priority * priority_weight) + \
                    (other_battery_score * battery_weight) + \
                    (other_distance_to_goal * distance_weight)
            
        print("robot_scores: ", robot_score, other_score)
        # Decision making for the entire aisle
        aisle_info = {
            "aisle_points": common_points,
            "entry_point": robot_entry_point,
            "robot_score": robot_score,
            "other_score": other_score,
            "other_robot": other_robot_name
        }
            
        if robot_score >= other_score:
            aisle_decisions.append(("FORWARD", aisle_info))
        else:
            aisle_decisions.append(("WAIT", aisle_info))
        
    # Compile results
    results = {
        "decision": "FORWARD" if all(d[0] == "FORWARD" for d in aisle_decisions) else "WAIT",
        "aisle_evaluations": aisle_decisions
    }
        
    return results["decision"]


robot1 = Robot(name="R1")
robot2 = Robot(name="R2")
# robot3 = Robot(name="R3", priority=3)

# Input from FMS

# CASE 1 - Common aisle
# path1 = [1, 2, 3, 4, 5, 12, 15, 16, 17, 18, 19]
# path2 = [10, 11, 12, 5, 4, 3, 6, 7]
# path3 = [1, 5, 6]

# CASE 2 - Just one common node
# if it is a common node we can just check when the other robot is coming, if the other robot's next node and current robot's next node is same only then it will be a problem
# so it conflict we have to separate it it is an aisle or just a common node
# also here comes one more point, in the path there can be multiple common aisles for two robots, when we are finding aisles we have to find that also
path1 = [1, 2, 3, 4, 5, 12, 13, 14, 9, 8, 7]
path2 = [10, 11, 12, 15, 16, 17, 18, 19]

robot1.handle_path(path1)
robot2.handle_path(path2)

robot1.update_priority(6)
robot2.update_priority(6)

robot1.update_battery_level(50)
robot2.update_battery_level(50)

robots = [
    robot1,
    robot2
]

start_time = time.time()

curr_robot = robot1
conflicts = find_conflicts(curr_robot, robots)
print("Conflicts found:", conflicts)
decision = handle_conflicts(conflicts, curr_robot)
print("Decision:", decision)

print("Time taken: ", time.time()-start_time)
