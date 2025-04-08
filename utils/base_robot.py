
# Robot class
class Robot:
    def __init__(self, name, priority, battery_lvl = 100):
        self.name = name
        self.current_pose = None
        self.priority = priority
        self.battery_level = battery_lvl
        self.full_path = None
        self.remaining_path = None
        self.current_node = None
        
        self.robot_speed = 2 # m/s
        self.total_load = None  # Total weight the robot is carrying
        self.total_items = None # Total no.of items robot is carrying

    def move(self):
        if self.stop_time is not None:
            print(f"[{self.name}] Waiting due to stop command until t={self.stop_time}")
            return
        if self.current_step < len(self.path):
            print(f"[{self.name}] Moving to node {self.path[self.current_step]}")
            self.current_step += 1
            
    def raise_request(self):    
        pass
        
        

# Sample setup
# robots = [
#     Robot(name="R1", path=[1, 2, 3, 4], priority=2),
#     Robot(name="R2", path=[4, 3, 2, 1], priority=1),
#     Robot(name="R3", path=[1, 5, 6], priority=3),
# ]


