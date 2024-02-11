class agent:
	def __init__(self, id):
		self.id = id
		
	def act(self, frame):
		raise NotImplemented("This is the base class, please inherit this")