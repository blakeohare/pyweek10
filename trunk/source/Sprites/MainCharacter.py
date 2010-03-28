
#TODO: split this into a parent sprite class when it comes time to make other enemies

class MainCharacter:
	
	def __init__(self, x, y):
		self.x = x # these points are the CENTER of the player
		self.y = y
		self.vy = 0
		self.vx = 0
		self.dx = 0
		self.dy = 0
		self.width = 16
		self.height = 24
		self.on_ground = False
		self.platform = None
		self.left_facing = False
	
	def get_top_left(self):
		x = int(self.x - self.width / 2)
		y = int(self.y - self.height / 2)
		return (x, y)
	
	def get_bottom(self):
		return self.get_top_left()[1] + self.height
	
	def get_left(self):
		return int(self.x - self.width / 2)
	
	def get_right(self):
		return self.get_left() + self.width
		
	def draw(self, surface, is_moving, counter):
		file = ('right', 'left')[self.left_facing]
		if is_moving:
			file += '_walk_' + str(int(int(counter / 3) % 3))
		else:
			file += '_stand'
		file += '.png'
		
		img = images.Get('sprites/MainChar/' + file)
		
		surface.blit(img, self.get_top_left())