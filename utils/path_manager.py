from typing import List, Dict, Any
from utils.base_robot import Robot
from utils.conflict_handler import ConflictDetector, ConflictResolver, Decision

class RobotPathManager:
    """Manages robot paths and conflict resolution."""
    
    def __init__(self, robots: List[Robot]):
        """
        Initialize with a list of robots.
        
        Args:
            robots: List of robots to manage
        """
        self.robots = robots
        self.conflict_detector = ConflictDetector()
        self.conflict_resolver = ConflictResolver()
        
    def make_decision(self, robot_name: str) -> str:
        """
        Make a movement decision for a robot.
        
        Args:
            robot_name: Name of the robot
            
        Returns:
            Decision (FORWARD or WAIT)
        """
        # Find the robot
        current_robot = None
        for robot in self.robots:
            if robot.name == robot_name:
                current_robot = robot
                break
        
        if not current_robot:
            raise ValueError(f"Robot '{robot_name}' not found")
        
        # Find conflicts and make decision
        conflicts = self.conflict_detector.find_conflicts(current_robot, self.robots)
        decision = self.conflict_resolver.handle_conflicts(conflicts, current_robot)
        
        return decision
    
    def move_robots(self) -> Dict[str, str]:
        """
        Decide movement for all robots and execute.
        
        Returns:
            Dictionary mapping robot names to their decisions
        """
        decisions = {}
        movements = {}
        
        # First, make decisions for all robots
        for robot in self.robots:
            if not robot.remaining_path:
                decisions[robot.name] = "DESTINATION_REACHED"
                movements[robot.name] = False
                continue
                
            decision = self.make_decision(robot.name)
            decisions[robot.name] = decision
            movements[robot.name] = False
        
        # Then, move robots based on decisions
        for robot in self.robots:
            if len(robot.remaining_path) > 0 and decisions[robot.name] == Decision.FORWARD.value:
                robot.move_forward()
                movements[robot.name] = True
                print(f"{robot.name} moved forward to {robot.current_node}")
            else:
                print(f"{robot.name} waiting at {robot.current_node}")
        
        return decisions
