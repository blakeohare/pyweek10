class Sprite:
	
	def __init__(self, x, y):
		self.x = x # these points are the CENTER of the player
		self.y = y
		self.vy = 0
		self.vx = 0
		self.dx = 0
		self.dy = 0
		self.width = 1
		self.height = 1
		self.on_ground = False
		self.platform = None
		self.left_facing = False
		self.moves_through_walls = False
		self.immune_to_gravity = False
		self.invincible = False
		self.confined_to_scene = False
		self.killed = False
		self.walked_into_wall = False
		self.is_soul_jar = False
	
	def get_collision_radius(self):
		return (self.width + self.height) / 2.0
	
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

	def is_collision_with_rect(self, left, right, top, bottom):
		tolerance = 2
		if self.get_left() + tolerance > right:
			return False
		if self.get_right() - tolerance < left:
			return False
		if self.get_top() + tolerance > bottom:
			return False
		if self.get_bottom() - tolerance < top:
			return False
		return True
	
	def GetPowerUp(self):
		return None #TODO: this		
	
	def platform_below_vx_location(self, playScene):
		x = self.x + (2 * self.vx)
		
		if self.platform != None:
			if self.platform.is_x_in_range(x):
				return True
			elif self.platform.left > x:
				left = playScene.get_left_stiched_platform(self.platform)
				if left != None: #TODO: will not handle things walking faster than 16 pixels/frame
					return left.is_x_in_range(x)
			else:
				right = playScene.get_right_stiched_platform(self.platform)
				if right != None:
					return right.is_x_in_range(x)
		return False
		
	def wall_at_vx_location(self, playScene):
		return self.walked_into_wall
	
	def is_going_to_vx_bad(self, playScene):
		return (
			self.platform != None and 
			not self.platform_below_vx_location(playScene)
			) or self.wall_at_vx_location(playScene)