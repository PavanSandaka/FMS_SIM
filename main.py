from utils.base_robot import Robot
from utils.path_manager import RobotPathManager
import time


# Example usage
def run_simulation():
    # Create robots
    robot1 = Robot(name="R1")
    robot2 = Robot(name="R2")
    robot3 = Robot(name="R3")
    
    # Set up paths
    # path1 = [3, 4, 5, 12, 13, 14, 9, 8, 7]
    # path2 = [10, 11, 12, 15, 16, 17, 18, 19]
    
    path1 = [1, 2, 3, 4, 5, 12, 15, 16, 17, 18, 19]
    path2 = [10, 11, 12, 5, 4, 3, 6, 7]
    path3 = [9, 14, 13, 12, 5, 4, 3, 2, 1]
    
    robot1.handle_path(path1)
    robot2.handle_path(path2)
    robot3.handle_path(path3)
    
    # Set priorities and battery levels
    robot1.update_priority(4)
    robot2.update_priority(6)
    robot3.update_priority(3)
    
    robot1.update_battery_level(50)
    robot2.update_battery_level(25)
    robot3.update_battery_level(50)
    
    robots = [robot1, robot2, robot3]
    # Create manager
    manager = RobotPathManager(robots)
    
    # Run simulation
    start_time = time.time()
    
    while True:
        print("\n--- Simulation step ---")
        
        # Make decisions and move robots
        decisions = manager.move_robots()
        
        # Print status
        for robot in robots:
            print(f"{robot.name} at node {robot.current_node}, decision: {decisions.get(robot.name, 'N/A')}")
            if robot.remaining_path:
                print(f"{robot.name} next node: {robot.next_node}")
            print(f"{robot.name} remaining path: {robot.remaining_path}")
            # print(f"{robot.name} full path: {robot.full_path}")

        break_flag = True
        # Check if simulation is complete
        for robot in robots:
            if len(robot.remaining_path)!=0:
                break_flag = False
                
        if break_flag:
            print("\nAll robots reached their destinations")
            break
        
        # Add delay for visualization
        time.sleep(2)
    
    print(f"Simulation completed in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    run_simulation()