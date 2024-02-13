from WSUSSL.TeamControl.Skills.baseskill import BaseSkill
import random
from WSUSSL.Shared.action import Action

# This is not ready to be used

class PathPlannerImport(BaseSkill):
    def __init__(self, world_model):
        print("This is still under development")
        super().__init__(world_model)
        self.add_state('start', self.start_action)
        self.add_state('run', self.run_action)
        self.add_state('finish', self.finish_action)
        self.start_state = 'start'
        self.final_state = 'finish'
        
        self.counter = 0

    def start_action(self):
        print("SampleSkill: Start action")
        # 1. take imports from path planner
        # 2. process it onto the skill
        # 3. compile and run action
        self.counter = 0
        self.transition_to('run')
        if random.randint(0,1):
            return Action(0,0,0,False,0)
        else:
            return Action(0,0,0,False,1.0)            

    def run_action(self):
        print("SampleSkill: Run action")
        self.counter += 1
        if self.counter > 10:
            self.transition_to('finish')
            
        return Action(0,1,0,False,0)
        
        
    def finish_action(self):
        print("SampleSkill: Finish action")
        return Action(0,0,0,False,0)        
