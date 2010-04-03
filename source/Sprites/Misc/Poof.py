class PoofCloud(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 15
		self.height = 11
		self.moves_through_walls = True
		self.immune_to_gravity = True
	
	def draw(self, surface, is_moving, counter, camera_offset):
		
		num = int(self.lifetime / 2.0) + 1
		num = max(1, min(5, num))
		file = 'poof/' + str(num) + '.png'
		img = images.Get(file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	
	def update(self, playScene):
		self.lifetime += 1
		if self.lifetime == 10:
			self.expired = True
