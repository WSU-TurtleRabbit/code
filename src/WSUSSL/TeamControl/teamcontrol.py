import sys
import os

from WSUSSL.World.model import Model as wm 
from WSUSSL.World.receiver import update_world_model
from WSUSSL.Shared.action import Action
from WSUSSL.TeamControl.Skills.sampleskill import SampleSkill

#import threading
import time

class TeamControl:
    def __init__(self, world_model, skills):
        self.world_model = world_model
        self.skills = skills  # A collection of skills
        self.current_skill = None
        #self.update_world_model = update_world_model(world_model)

    def select_skill(self):
        # Logic to select the appropriate skill based on the world model
        self.current_skill = skills[0]
        self.current_skill.initialise()

    def run_skill_loop(self):
        self.select_skill()
        while not self.current_skill.is_final():
            print("skill loop")
            a = self.current_skill.execute()
            # todo: now send this action to the robot
            time.sleep(5)  # Skill execution rate

    def start(self):
        # Start the WorldModel update loop in a separate thread
        #threading.Thread(target=self.update_world_model).start()

        # Start the skill execution loop
        self.run_skill_loop()

if __name__ == '__main__':
    # Example usage:
    world_model = wm(isYellow=True)
    skill1 = SampleSkill(world_model)
    skills = [skill1]
    # tc = TeamControl(world_model, skills)
    # tc.start()

