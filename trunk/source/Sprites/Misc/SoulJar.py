class SoulJar(Sprite):
	
	def __init__(self, x, y, random_number):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 8
		self.height = 8
		self.vx = 9 * (-1, 1)[int(random_number % 2)]
		self.vy = -5
		self.confined_to_scene = True
		self.is_soul_jar = True
	
	def draw(self, surface, is_moving, counter, camera_offset):
		
		file = 'sprites/mumblefoo/mumblefoo' + str(int(counter % 8)) + '.png'
		img = images.Get(file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	
	def update(self, playScene):
		self.lifetime += 1
		if self.vx > 0:
			self.vx = max(0, self.vx - .4)
		elif self.vx < 0:
			self.vx = min(0, self.vx + .4)
