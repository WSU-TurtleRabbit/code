from worldmodel import WorldModel
from shared.action import Action

import threading
import time

class TeamControl:
    def __init__(self, world_model, skills):
        self.world_model = world_model
        self.skills = skills  # A collection of skills
        self.current_skill = None

    def select_skill(self):
        # Logic to select the appropriate skill based on the world model
        pass

    def run_skill_loop(self):
        while True:
            print("skill loop")
            time.sleep(5)  # Skill execution rate

    def start(self):
        # Start the WorldModel update loop in a separate thread
        threading.Thread(target=self.world_model.update_loop).start()

        # Start the skill execution loop
        self.run_skill_loop()

# Example usage:
world_model = WorldModel()
skills = None
tc = TeamControl(world_model, skills)
tc.start()

