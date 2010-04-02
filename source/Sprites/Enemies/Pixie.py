
class EnemyPixie(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 16
		self.height = 16
		self.left_facing = True
		self.immune_to_gravity = True
		
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('Right', '')[self.left_facing]
		
		file = direction + 'fly' + str(int(int(counter / 3) % 3)) + '.png'
		
		img = images.Get('sprites/Enemies/Pixie/' + file)
		
		xy = self.get_top_left()
		img_offset = images.GetOffset(img)
		x = xy[0] - camera_offset[0] + img_offset[0]
		y = xy[1] - camera_offset[1] + img_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		
