__all__ = []

class BaseSkill:
    def __init__(self, world_model):
        self.states = {}
        self.current_state = None  # Initialize current state
        self.world_model = world_model
        self.start_state = None
        self.final_state = None
        
    def add_state(self, state: str, function: callable=None):
        """Adding states and associated function to the skill script."""
        self.states[state] = function
        
    def set_state(self, state: str):
        if state not in self.states:
            raise ValueError("State not found in skill.")
        self.current_state = state  

    def get_state(self):
        """Return the current state"""
        return self.current_state

    def initialise(self):
        self.set_state(self.start_state)

    def is_final(self):
        # check the current state is final;
        # might be better to also check if final_state is defined
        if not isinstance(self.final_state, callable):
            return ValueError, f"self.final_state in skill {__class__} is not defined"
        return self.current_state is self.final_state

    def transition_to(self,state):
        """Move from one sttae of the skill to the next state"""
        if state not in self.states:
            raise ValueError("State not found in skill.")
        self.current_state = state  
            
    def execute(self):
        """Executes the current state's action."""
        if self.current_state not in self.states:
            raise ValueError("Current state is not in the state machine")

        # Execute the state's action
        state_function = self.states[self.current_state]
        if callable(state_function):
            state_function()
        else:
            raise NotImplementedError(f'Action for state {self.current_state} is not implemented')
            
