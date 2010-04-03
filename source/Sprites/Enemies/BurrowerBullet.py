
class EnemyBurrowerBullet(Sprite):
	
	def __init__(self, x, y, vx):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 4
		self.height = 4
		self.vx = vx
		self.immune_to_gravity = True
		self.moves_through_walls = True
		self.invincible = True
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		if self.lifetime > 60 and int(self.lifetime % 2) == 0:
			return
		
		img = images.Get('sprites/Enemies/Burrower/bullet.png')
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		self.x += self.vx
		if self.lifetime > 90:
			self.expired = True
			
		