class Sprite:
	
	def __init__(self, x, y):
		self.x = x # these points are the CENTER of the player
		self.y = y
		self.vy = 0
		self.vx = 0
		self.dx = 0
		self.dy = 0
		self.width = 14
		self.height = 30
		self.on_ground = False
		self.platform = None
		self.left_facing = False
	
	def get_top_left(self):
		return (self.get_left(), self.get_top())
	
	def get_left(self):
		return int(self.x - self.width / 2)
	
	def get_top(self):
		return int(self.y - self.height / 2)
	
	def get_head_bonk_top(self):
		return int(self.y - self.height / 2) + 5
	
	def get_bottom(self):
		return self.get_top_left()[1] + self.height
	
	def get_left(self):
		return int(self.x - self.width / 2)
	
	def get_right(self):
		return self.get_left() + self.width
		
	def update(self, playScene):
		pass


