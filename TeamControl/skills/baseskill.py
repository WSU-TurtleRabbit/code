class BaseSkill:
    def __init__(self, world_model):
        self.current_state = None  # Initialize current state
        self.world_model = None
        
    def set_state(self, state):
        self.current_state = state  # Method to set the current state

    def get_state(self):
        return self.current_state  # Method to get the current state

    def execute(self):
        # Override this method in subclasses to implement specific skill logic
        # It should return an Action instance based on the current state
        raise NotImplementedError("This method should be overridden by subclasses")


            
