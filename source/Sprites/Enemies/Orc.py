
class EnemyOrc(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 15
		self.height = 32
		self.left_facing = True
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('right', 'left')[self.left_facing]
		
		file = direction + str(int(int(counter / 4) % 3)) + '.png'
		
		img = images.Get('sprites/Enemies/Orclike/' + file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		
		self.vx = (1, -1)[self.left_facing]
		if self.is_going_to_vx_bad(playScene):
			self.vx *= -1
			self.left_facing = not self.left_facing
	