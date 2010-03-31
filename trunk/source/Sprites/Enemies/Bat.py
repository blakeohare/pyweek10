
class EnemyBat(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.left_facing = True
		self.immune_to_gravity = True
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('Right', 'Left')[self.left_facing]
		
		file = direction + 'Bat' + ('','MidFlap','DownFlap','MidFlap')[int(int(counter / 3) % 4)] + '.png'
		
		img = images.Get('sprites/Enemies/Bat/' + file)
		
		xy = self.get_top_left()
		img_offset = images.GetOffset(img)
		x = xy[0] - camera_offset[0] + img_offset[0]
		y = xy[1] - camera_offset[1] + img_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		self.vx = -2
