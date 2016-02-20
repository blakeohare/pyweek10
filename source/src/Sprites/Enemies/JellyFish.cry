
class EnemyJellyFish(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = int((7 * int(x / 16.0) + int(y / 13.0)) % 60)
		Sprite.__init__(self, x, y)
		self.width = 16
		self.height = 16
		self.center_x = x
		self.center_y = y
		self.squirt_range = 16
		self.left_facing = True
		self.immune_to_gravity = True
		self.image = '0'
	def draw(self, surface, is_moving, counter, camera_offset):
		
		img = images.Get('sprites/Enemies/Jellyfish/' + self.image + '.png')
		
		xy = self.get_top_left()
		img_offset = images.GetOffset(img)
		x = xy[0] - camera_offset[0] + img_offset[0]
		y = xy[1] - camera_offset[1] + img_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		
		x_offset = math.sin(self.lifetime * 2 * 3.14159265 / 300) * 16
		self.x = int(self.center_x + x_offset)
		
		#drift down
		if self.lifetime % 60 < 40: 
			progress = (self.lifetime % 60.0) / 40.0
			if progress > 0.8:
				self.image = '1'
			else:
				self.image = '0'
		#squirt up
		else:
			self.image = '2'
			progress = ((self.lifetime % 60.0) - 40) / 20.0
			progress = 1 - progress
		distance = (progress * 2 - 1.0)
		self.y = int(self.center_y + distance * self.squirt_range)