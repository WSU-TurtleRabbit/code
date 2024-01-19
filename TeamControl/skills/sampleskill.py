from baseskill import BaseSkill

class SampleSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.add_state('start', self.start_action)
        self.add_state('run', self.run_action)
        self.add_state('finish', self.finish_action)

        self.counter = 0

    def start_action(self):
        print("SampleSkill: Start action")

        self.counter = 0
        
        if random.randint():
            self.transition_to('finish')
            return Action(0,0,0,False,0)
        else:
            self.transition_to('run')
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
        

    def run_action
        
