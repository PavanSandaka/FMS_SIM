from enum import Enum
from typing import List, Dict, Tuple, Any
from utils.base_robot import Robot


class ConflictType(Enum):
    """Enum to represent different types of conflicts."""
    NODE = "NODE"
    AISLE = "AISLE"


class Direction(Enum):
    """Enum to represent direction of travel through an aisle."""
    SAME = "SAME"
    OPPOSITE = "OPPOSITE"
    UNKNOWN = "UNKNOWN"


class Decision(Enum):
    """Enum to represent possible decisions."""
    FORWARD = "FORWARD"
    WAIT = "WAIT"


class ConflictDetector:
    """Responsible for detecting conflicts between robots."""
    
    @staticmethod
    def find_connected_aisles(robot1: Robot, robot2: Robot) -> List[List[Any]]:
        """
        Find connected segments of common path points and identify them as aisles.
        
        Args:
            robot1: First robot
            robot2: Second robot
            
        Returns:
            List of aisles (lists of connected points)
        """
        common_points = set(robot1.full_path) & set(robot2.full_path)
        
        # No common points, no aisles
        if not common_points:
            return []
        
        # Get indices of common points in both paths
        r1_indices = {point: idx for idx, point in enumerate(robot1.full_path) if point in common_points}
        r2_indices = {point: idx for idx, point in enumerate(robot2.full_path) if point in common_points}
        
        # Group common points into connected aisles
        aisles = []
        current_aisle = []
        
        # Sort common points by their position in robot1's path
        sorted_common_points = sorted(common_points, key=lambda p: r1_indices[p])
        
        for point in sorted_common_points:
            # Start a new aisle or continue current one
            if not current_aisle:
                current_aisle = [point]
            else:
                # Check if points are adjacent in either robot's path
                prev_point = current_aisle[-1]
                
                # Check adjacency in robot1's path
                r1_adjacent = abs(r1_indices[point] - r1_indices[prev_point]) == 1
                # Check adjacency in robot2's path
                r2_adjacent = abs(r2_indices[point] - r2_indices[prev_point]) == 1
                
                if r1_adjacent or r2_adjacent:
                    # Points are adjacent, continue the aisle
                    current_aisle.append(point)
                else:
                    # Points are not adjacent, start a new aisle
                    if current_aisle:
                        aisles.append(current_aisle)
                    current_aisle = [point]
        
        # Add the last aisle if not empty
        if current_aisle:
            aisles.append(current_aisle)
        
        return aisles
    
    @staticmethod
    def is_next_move_into_conflict(robot: Robot, conflict_points: List[Any]) -> bool:
        """
        Check if the robot's next move will lead it into a conflict zone.
        
        Args:
            robot: The robot to check
            conflict_points: Points in the conflict zone
            
        Returns:
            True if next move is into conflict, False otherwise
        """
        if not robot.remaining_path:
            return False
        
        # Check if the next node is in the conflict points
        return robot.next_node in conflict_points
    
    @staticmethod
    def steps_to_conflict(robot: Robot, conflict_points: List[Any]) -> int:
        """
        Calculate how many steps until the robot reaches the conflict zone.
        
        Args:
            robot: The robot to check
            conflict_points: Points in the conflict zone
            
        Returns:
            Number of steps to reach conflict (-1 if no conflict)
        """
        for idx, point in enumerate(robot.full_path):
            if point in conflict_points:
                return idx
        return -1
    
    @staticmethod
    def determine_aisle_direction(
        robot: Robot, 
        other_robot: Robot, 
        aisle_points: List[Any]
    ) -> Direction:
        """
        Determine if robots are traveling in the same or opposite directions through the aisle.
        
        Args:
            robot: First robot
            other_robot: Second robot
            aisle_points: Points in the aisle
            
        Returns:
            Direction enum indicating if robots are traveling in the same or opposite direction
        """
        if len(aisle_points) < 2:
            return Direction.UNKNOWN  # Can't determine direction for single-point aisles
        
        # Find first and last point each robot encounters in the aisle
        robot_aisle_indices = [i for i, p in enumerate(robot.full_path) if p in aisle_points]
        other_aisle_indices = [i for i, p in enumerate(other_robot.full_path) if p in aisle_points]
        
        if not robot_aisle_indices or not other_aisle_indices:
            return Direction.UNKNOWN
        
        robot_first_point = robot.full_path[min(robot_aisle_indices)]
        robot_last_point = robot.full_path[max(robot_aisle_indices)]
        
        other_first_point = other_robot.full_path[min(other_aisle_indices)]
        other_last_point = other_robot.full_path[max(other_aisle_indices)]
        
        # If first/last points are the same for both robots but in opposite order, they're traveling in opposite directions
        if robot_first_point == other_last_point and robot_last_point == other_first_point:
            return Direction.OPPOSITE
        
        # Get aisle points in sequence for each robot
        robot_aisle_path = [robot.full_path[i] for i in sorted(robot_aisle_indices)]
        other_aisle_path = [other_robot.full_path[i] for i in sorted(other_aisle_indices)]
        
        # Check if the sequences are the same or reverse of each other
        if robot_aisle_path == other_aisle_path:
            return Direction.SAME
        elif robot_aisle_path == list(reversed(other_aisle_path)):
            return Direction.OPPOSITE
        
        # If can't clearly determine, check first and last points positions in the aisle
        aisle_sequence = list(aisle_points)
        try:
            robot_first_idx = aisle_sequence.index(robot_first_point)
            robot_last_idx = aisle_sequence.index(robot_last_point)
            other_first_idx = aisle_sequence.index(other_first_point)
            other_last_idx = aisle_sequence.index(other_last_point)
            
            # If slope of indices is the same, they're moving in the same direction
            robot_direction = robot_last_idx - robot_first_idx
            other_direction = other_last_idx - other_first_idx
            
            if (robot_direction * other_direction) > 0:  # Same sign means same direction
                return Direction.SAME
            else:
                return Direction.OPPOSITE
        except ValueError:
            return Direction.UNKNOWN
    
    @staticmethod
    def find_conflicts(robot: Robot, robots: List[Robot]) -> List[Dict]:
        """
        Find all conflicts between the given robot and all other robots.
        
        Args:
            robot: The robot to check conflicts for
            robots: List of all robots in the system
            
        Returns:
            List of conflict dictionaries with immediate relevance flag
        """
        conflicts = []
        
        # Check for conflict with the current robot with all the other robots
        for other_robot in robots:
            # Skip comparing the robot with itself
            if other_robot.name == robot.name:
                continue
            
            # Check if robot's next node is the current position of other robot
            if robot.next_node and robot.next_node == other_robot.current_node:
                # Immediate collision risk - the node is already occupied
                conflicts.append({
                    "robot": other_robot.name,
                    "robot_obj": other_robot,
                    "conflict_points": [robot.next_node],
                    "conflict_type": ConflictType.NODE,
                    "is_immediate": True,
                    "steps_to_conflict": 0,
                    "other_steps_to_conflict": 0,
                    "node_occupied": True,  # Flag to indicate node is currently occupied
                    "direction": Direction.UNKNOWN  # Direction doesn't matter for occupied nodes
                })
                
            # Find connected aisles that are common in both paths
            aisles = ConflictDetector.find_connected_aisles(robot, other_robot)
            
            print(f"Found {len(aisles)} aisles between {robot.name} and {other_robot.name}")
            
            if aisles:
                for aisle in aisles:
                    # Classify as single node or aisle
                    conflict_type = ConflictType.NODE if len(aisle) == 1 else ConflictType.AISLE
                    
                    # Check if the next move leads to this conflict
                    is_immediate = ConflictDetector.is_next_move_into_conflict(robot, aisle)
                    steps_to_conflict = ConflictDetector.steps_to_conflict(robot, aisle)
                    
                    # Check if other robot is also heading to this conflict
                    other_steps = ConflictDetector.steps_to_conflict(other_robot, aisle)
                    other_heading_to_conflict = other_steps >= 0
                    
                    # Only consider conflicts if both robots are heading toward the same aisle
                    if not other_heading_to_conflict:
                        continue
                    
                    # Determine direction of travel
                    direction = Direction.UNKNOWN
                    if conflict_type == ConflictType.AISLE:
                        direction = ConflictDetector.determine_aisle_direction(robot, other_robot, aisle)
                    
                    conflicts.append({
                        "robot": other_robot.name,
                        "robot_obj": other_robot,
                        "conflict_points": aisle,
                        "conflict_type": conflict_type,
                        "is_immediate": is_immediate,
                        "steps_to_conflict": steps_to_conflict,
                        "other_steps_to_conflict": other_steps,
                        "node_occupied": False,
                        "direction": direction
                    })
        
        return conflicts


class ConflictResolver:
    """Responsible for resolving conflicts between robots."""
    
    # Default weights for scoring
    DEFAULT_WEIGHTS = {
        "proximity": 0.4,
        "priority": 0.3,
        "battery": 0.2,
        "distance": 0.1
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize with custom weights if provided.
        
        Args:
            weights: Custom weights for scoring factors
        """
        self.weights = weights or self.DEFAULT_WEIGHTS
    
    @staticmethod
    def find_entry_point_to_aisle(robot: Robot, aisle_points: List[Any]) -> Tuple[int, Any]:
        """
        Find the first point in the robot's path that's part of the aisle.
        
        Args:
            robot: The robot to check
            aisle_points: Points in the aisle
            
        Returns:
            Tuple of (entry_index, entry_point)
        """
        entry_index = float('inf')
        entry_point = None
            
        for point in aisle_points:
            try:
                index = robot.full_path.index(point)
                if index < entry_index:
                    entry_index = index
                    entry_point = point
            except ValueError:
                continue
            
        return entry_index, entry_point
    
    def calculate_node_conflict_scores(
        self, 
        robot: Robot, 
        other_robot: Robot
    ) -> Tuple[float, float]:
        """
        Calculate scores for node conflict resolution.
        
        Args:
            robot: First robot
            other_robot: Second robot
            
        Returns:
            Tuple of (robot_score, other_score)
        """
        # Extract scoring factors
        robot_priority = robot.task_priority
        other_priority = other_robot.task_priority
        
        robot_battery = robot.battery_lvl
        other_battery = other_robot.battery_lvl
        
        robot_distance_to_goal = len(robot.remaining_path)
        other_distance_to_goal = len(other_robot.remaining_path)

        # Battery score - lower battery means higher score
        robot_battery_score = (100 - robot_battery) / 100
        other_battery_score = (100 - other_battery) / 100
            
        # Calculate composite scores
        robot_score = (robot_priority * self.weights["priority"]) + \
                    (robot_battery_score * self.weights["battery"]) + \
                    (robot_distance_to_goal * self.weights["distance"])
                        
        other_score = (other_priority * self.weights["priority"]) + \
                    (other_battery_score * self.weights["battery"]) + \
                    (other_distance_to_goal * self.weights["distance"])
                    
        return robot_score, other_score
    
    def calculate_aisle_conflict_scores(
        self, 
        robot: Robot, 
        other_robot: Robot,
        robot_entry_index: int,
        other_entry_index: int,
        direction: Direction
    ) -> Tuple[float, float]:
        """
        Calculate scores for aisle conflict resolution, considering direction of travel.
        
        Args:
            robot: First robot
            other_robot: Second robot
            robot_entry_index: Entry index for first robot
            other_entry_index: Entry index for second robot
            direction: Direction of travel through aisle
            
        Returns:
            Tuple of (robot_score, other_score)
        """
        # If robots are moving in the same direction, prioritize the closer one
        if direction == Direction.SAME:
            # Simple comparison of entry indices - lower is better
            if robot_entry_index < other_entry_index:
                print(f"Same direction conflict: {robot.name} is closer to aisle than {other_robot.name}")
                return 1.0, 0.0  # First robot gets priority
            elif robot_entry_index > other_entry_index:
                print(f"Same direction conflict: {other_robot.name} is closer to aisle than {robot.name}")
                return 0.0, 1.0  # Second robot gets priority
            else:
                print(f"Same direction conflict but equal distance - falling back to normal scoring")
                # Fall back to normal scoring if they're equidistant
        
        # Extract scoring factors
        robot_priority = robot.task_priority
        other_priority = other_robot.task_priority
        
        robot_battery = robot.battery_lvl
        other_battery = other_robot.battery_lvl
        
        # Calculate distance to goal
        robot_distance_to_goal = len(robot.full_path) - robot_entry_index if robot_entry_index != float('inf') else 0
        other_distance_to_goal = len(other_robot.full_path) - other_entry_index if other_entry_index != float('inf') else 0
        
        # Convert proximity to a score where closer is better
        robot_proximity_score = 1/(robot_entry_index+1) if robot_entry_index != float('inf') else 0
        other_proximity_score = 1/(other_entry_index+1) if other_entry_index != float('inf') else 0
        
        # Battery score - lower battery means higher score
        robot_battery_score = (100 - robot_battery) / 100
        other_battery_score = (100 - other_battery) / 100
        
        # Calculate composite scores
        robot_score = (robot_proximity_score * self.weights["proximity"]) + \
                    (robot_priority * self.weights["priority"]) + \
                    (robot_battery_score * self.weights["battery"]) + \
                    (robot_distance_to_goal * self.weights["distance"])
                    
        other_score = (other_proximity_score * self.weights["proximity"]) + \
                    (other_priority * self.weights["priority"]) + \
                    (other_battery_score * self.weights["battery"]) + \
                    (other_distance_to_goal * self.weights["distance"])
        
        return robot_score, other_score
    
    def handle_conflicts(self, conflicts: List[Dict], robot: Robot) -> str:
        """
        Handle conflicts and make a decision.
        
        Args:
            conflicts: List of conflicts
            robot: The robot to make a decision for
            
        Returns:
            Decision (FORWARD or WAIT)
        """
        if not conflicts:
            return Decision.FORWARD.value  # No conflicts, robot can proceed
            
        # Filter to only immediate conflicts - where next move leads into conflict
        immediate_conflicts = [c for c in conflicts if c["is_immediate"]]
        
        # If there are no immediate conflicts, the robot can proceed
        if not immediate_conflicts:
            return Decision.FORWARD.value
        
        # Check first for occupied nodes - highest priority conflicts
        occupied_node_conflicts = [c for c in immediate_conflicts if c.get("node_occupied", False)]
        if occupied_node_conflicts:
            # Node is occupied, must wait
            return Decision.WAIT.value
        
        aisle_decisions = []
            
        for conflict in immediate_conflicts:
            other_robot_name = conflict["robot"]
            other_robot = conflict["robot_obj"]
            conflict_points = conflict["conflict_points"]
            conflict_type = conflict["conflict_type"]
            direction = conflict.get("direction", Direction.UNKNOWN)
            
            # Check if the conflict points are still in the remaining paths
            if not (set(conflict_points) & set(robot.remaining_path) & set(other_robot.remaining_path)):
                print("----No Intersection-------")
                print(f"conflict points: {conflict_points}")
                print("***can skip this conflict***\n")
                continue
                
            # Handle NODE conflict
            if conflict_type == ConflictType.NODE:
                # Check if robots are heading to the same next node
                if robot.next_node != other_robot.next_node:
                    print("No immediate conflict at node - can move forward!")
                    continue
                
                # Calculate scores for NODE conflict
                robot_score, other_score = self.calculate_node_conflict_scores(robot, other_robot)
                
                print(f"Node conflict scores with {other_robot_name}: {robot_score:.4f} vs {other_score:.4f}")
                
                # Create aisle info
                aisle_info = {
                    "aisle_points": conflict_points,
                    "aisle_type": conflict_type.value,
                    "robot_score": robot_score,
                    "other_score": other_score,
                    "other_robot": other_robot_name,
                    "direction": direction.value if direction else Direction.UNKNOWN.value
                }
                
                # Make decision based on scores
                if robot_score > other_score:
                    aisle_decisions.append((Decision.FORWARD.value, aisle_info))
                elif robot_score < other_score:
                    aisle_decisions.append((Decision.WAIT.value, aisle_info))
                else:
                    # Scores are equal, use name-based tie-breaker
                    if robot.name < other_robot.name:
                        print(f"Tie resolved: {robot.name} gets priority over {other_robot.name}")
                        aisle_decisions.append((Decision.FORWARD.value, aisle_info))
                    else:
                        print(f"Tie resolved: {other_robot.name} gets priority over {robot.name}")
                        aisle_decisions.append((Decision.WAIT.value, aisle_info))
                
                continue
            
            # Handle AISLE conflict
            # Find entry points to the aisle for both robots
            robot_entry_index, robot_entry_point = self.find_entry_point_to_aisle(robot, conflict_points)
            other_entry_index, other_entry_point = self.find_entry_point_to_aisle(other_robot, conflict_points)
            
            if conflict_type == ConflictType.AISLE and direction == Direction.SAME:
                print(f"Same direction aisle conflict with {other_robot_name}")
    
                # Check if robots would collide
                if robot.next_node == other_robot.current_node:
                    # Would move to the same node as other robot - must wait
                    print(f"Would collide with {other_robot_name}, must wait")
                    return Decision.WAIT.value
        
                # If both robots are targeting the same next node, resolve based on priority
                if robot.next_node == other_robot.next_node:
                    # Calculate scores to determine priority
                    robot_score, other_score = self.calculate_node_conflict_scores(robot, other_robot)
        
                    if robot_score <= other_score:
                        print(f"{other_robot_name} has higher priority for same next node")
                        return Decision.WAIT.value
                    else:
                        print(f"{robot.name} has higher priority, can proceed")
                        # Continue checking other conflicts
    
                # If no immediate collision risk, allow robots to follow each other in the aisle
                print(f"Same direction, can safely proceed through aisle")
                # Continue checking other conflicts by creating a FORWARD decision
                aisle_info = {
                    "aisle_points": conflict_points,
                    "aisle_type": conflict_type.value,
                    "entry_point": robot_entry_point,
                    "other_robot": other_robot_name,
                    "direction": direction.value
                }
                aisle_decisions.append((Decision.FORWARD.value, aisle_info))
                continue  # Skip the standard aisle conflict resolution below
                        
            # Calculate scores for AISLE conflict, considering direction
            robot_score, other_score = self.calculate_aisle_conflict_scores(
                robot, other_robot, robot_entry_index, other_entry_index, direction
            )
            
            print(f"Aisle conflict scores with {other_robot_name} ({direction.value}): {robot_score:.4f} vs {other_score:.4f}")
            
            # Create aisle info
            aisle_info = {
                "aisle_points": conflict_points,
                "aisle_type": conflict_type.value,
                "entry_point": robot_entry_point,
                "robot_score": robot_score,
                "other_score": other_score,
                "other_robot": other_robot_name,
                "direction": direction.value if direction else Direction.UNKNOWN.value
            }
            
            # Make decision based on scores
            if robot_score > other_score:
                aisle_decisions.append((Decision.FORWARD.value, aisle_info))
            elif robot_score < other_score:
                aisle_decisions.append((Decision.WAIT.value, aisle_info))
            else:
                # Scores are equal, use name-based tie-breaker
                if robot.name < other_robot.name:
                    print(f"Tie resolved: {robot.name} gets priority over {other_robot.name}")
                    aisle_decisions.append((Decision.FORWARD.value, aisle_info))
                else:
                    print(f"Tie resolved: {other_robot.name} gets priority over {robot.name}")
                    aisle_decisions.append((Decision.WAIT.value, aisle_info))
        
        print(f"Decisions for immediate conflicts: {aisle_decisions}")
        
        # Compile results - WAIT if any conflict requires waiting
        final_decision = Decision.FORWARD.value if all(d[0] == Decision.FORWARD.value for d in aisle_decisions) else Decision.WAIT.value
        
        return final_decision
