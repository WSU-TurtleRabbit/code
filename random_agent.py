from agent import agent
import random

class RandomAgent(agent):
	def act(self, frame):
		self.vx = random.random()
		self.vy = random.random()
		self.vz = random.random()
		return self.id, self.vx, self.vy, self.vz