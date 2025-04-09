
# Robot class
class Robot:
    def __init__(self, name, battery_lvl = 100):
        self.name = name
        self.battery_lvl = battery_lvl
        
        self.current_pose = None
        self.full_path = None
        self.remaining_path = None
        
        self.current_node = None
        self.next_node = None
        
        self.task_priority = None
        
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
    
    def handle_path(self, path):
        self.full_path = path
        self.remaining_path = path
        self.current_node = self.remaining_path.pop(0)
        self.next_node = self.remaining_path[0]
        
    def update_battery_level(self, lvl):
        self.battery_lvl = lvl
        
    def update_priority(self, priority):
        self.task_priority = priority 
        
    def move_forward(self):
        self.current_node = self.remaining_path.pop(0)
        if len(self.remaining_path)>1:
            self.next_node = self.remaining_path[0]
        else:
            self.next_node = None
          
    def raise_request(self):    
        pass
        
        

# Sample setup
# robots = [
#     Robot(name="R1", path=[1, 2, 3, 4], priority=2),
#     Robot(name="R2", path=[4, 3, 2, 1], priority=1),
#     Robot(name="R3", path=[1, 5, 6], priority=3),
# ]


