class Platform:
	def __init__(self, type, left, y_left, width, y_right, height, jumpthrough):
		self.type = type # jumpthrough, blocking, solid, incline
		self.left = left
		self.y_left = y_left
		self.width = width
		self.height = height # only used for solid type
		self.y_right = y_right
		self.jumpthrough = jumpthrough
	
	def duplicate(self, x_offset, y_offset):
		return Platform(self.type,
			self.left + x_offset,
			self.y_left + y_offset,
			self.width,
			self.y_right + y_offset,
			self.height,
			self.jumpthrough)
	
	def get_y_at_x(self, x):
		if self.type == 'incline':
			percentage = (x - self.left + 0.0) / self.width
			return int(self.y_right * percentage + self.y_left * (1 - percentage))
		return self.y_left
	
	def get_x_at_y(self, y):
		# this method is for INCLINES only
		# y MUST be in the range of this incline
		percentage = (y - self.y_left + 0.0) / (self.y_right - self.y_left)
		return int(self.left + percentage * self.width)
	
	def is_x_in_range(self, x):
		return self.left <= x and self.left + self.width >= x
	
	def get_left_wall_x(self):
		return self.left
	
	def get_right_wall_x(self):
		return self.left + self.width
	
	def get_top(self): #assumes non incline type
		return self.y_left 
	
	def get_bottom(self):
		if self.type == 'solid':
			return self.y_left + self.height
		return self.y_left #inclines aren't "bottomed"
	
	def get_closest_terminating_y(self, x):
		if x < self.left:
			return self.y_left
		else:
			return self.y_right
		# this function will not be called when x is in the platform
