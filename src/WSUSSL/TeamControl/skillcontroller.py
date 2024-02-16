import sys
import os

from WSUSSL.World.model import Model as wm 
from WSUSSL.Shared.action import Action
from WSUSSL.TeamControl.Skills.sampleskill import SampleSkill

#import threading
import time

class SkillControl:
    def __init__(self, world_pipe, skills):
        """_summary_
            Skill Control requires an array of skill callables
            Skill control will then initiate skills
            Skills will then begin stages : start run finish
            Skills completed will then move onto the next. 
        Args:
            world_pipe (pipe): the multiprocessing pipe : world model from receiver
            skills (tuple): an array of skill names
        """
        self.world_pipe = world_pipe
        self.skills = skills  # A collection of skills
        self.current_skill = None
        self.world_model = None
        self.skill_pipe = None

    # def get_world_update(self):
    #     while True:
    #         self.world_model = self.world_pipe.recv()

    def select_skill(self, world_model):
        # Logic to select the appropriate skill based on the world model
        self.current_skill = self.skills[0](world_model)
        print("Initialising skills now.")
        self.current_skill.initialise()

    def run_skill_loop(self):
        while True:
            # if there is data in the pipe.
            if self.world_pipe.poll():
                # updates world model
                self.world_model = self.world_pipe.recv()
                print("Selecting skills")
                self.select_skill(self.world_model)
                if not self.current_skill.is_final():
                    print("sending skills")
                    action = self.current_skill.execute()
                    print(action)
                    # self.skill_pipe.send(action)

                    # todo: now send this action to the robot
                    time.sleep(1)  # Skill execution rate

    def start(self):
        # Start the WorldModel update loop in a separate thread
        #threading.Thread(target=self.update_world_model).start()

        # Start the skill execution loop
        self.run_skill_loop()

    def pipe(self):
        from multiprocessing import Pipe
        self.skill_pipe, _ = Pipe()
        return _

if __name__ == '__main__':
    pass
    # Example usage:
    #world_model = wm(isYellow=True)
    # skill1 = SampleSkill(world_model)
    # skills = [skill1]
    # tc = TeamControl(world_model, skills)
    # tc.start()

