class agent:
	def __init__(self, id):
		self.id = id

	def check_boundary(self, position):
		'''
			Checks whether a position is within the field boundaries. 
		'''
		field_length = 5040 #mm
		field_width = 2760 #mm
		safety_border = 500 #mm # large because robot does not know where it is close to the edges of the field
		if position[0] < 0:
			position[0] = max(-field_length/2+safety_border, position[0])
		else:
			position[0] = min(field_length/2-safety_border, position[0])

		if position[1] < 0:
			position[1] = max(-field_width/2+safety_border, position[1])
		else:
			position[1] = min(field_width/2-safety_border, position[1])
		
		return position
		
	def act(self, frame):
		raise NotImplemented("This is the base class, please inherit this")