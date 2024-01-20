import sys
import os

# Addding the 'shared' and 'TeamControl' dirs to sys.path
shared_dir = os.path.abspath('../shared')
sys.path.append(shared_dir)

teamcontrol_dir = os.path.abspath('../TeamControl')
sys.path.append(teamcontrol_dir)

from worldmodel import WorldModel
from action import Action
from skills.sampleskill import SampleSkill

import threading
import time

class TeamControl:
    def __init__(self, world_model, skills):
        self.world_model = world_model
        self.skills = skills  # A collection of skills
        self.current_skill = None

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
        threading.Thread(target=self.world_model.update_loop).start()

        # Start the skill execution loop
        self.run_skill_loop()

# Example usage:
world_model = WorldModel()
skill1 = SampleSkill(world_model)
skills = [skill1]
tc = TeamControl(world_model, skills)
tc.start()

