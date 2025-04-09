
# Robot class
class Robot:
    def __init__(self, name, battery_lvl = 100):
        self.name = name
        self.battery_lvl = battery_lvl
        
        self.current_pose = None
        self.waiting = False
        
        self.full_path = None
        self.remaining_path = None
        
        self.current_node = None
        self.next_node = None
        
        self.task_priority = None
        
        self.robot_speed = 2 # m/s
        self.total_load = None  # Total weight the robot is carrying
        self.total_items = None # Total no.of items robot is carrying
    
    def handle_path(self, path):
        self.full_path = path.copy()  # Create a copy for full_path
        self.remaining_path = path.copy()  # Create another copy for remaining_path
        self.current_node = self.remaining_path.pop(0)
        self.next_node = self.remaining_path[0] if self.remaining_path else None
        
    def update_battery_level(self, lvl):
        self.battery_lvl = lvl
        
    def update_priority(self, priority):
        self.task_priority = priority 
        
    def move_forward(self):
        self.current_node = self.remaining_path.pop(0)
        if len(self.remaining_path)>0:
            self.next_node = self.remaining_path[0]
        else:
            self.next_node = None
          
    def reset_robot(self):
        self.full_path = None
        self.remaining_path = None
        self.current_node = None
        self.next_node = None
        self.current_pose = None
        
    def raise_request(self):    
        pass
