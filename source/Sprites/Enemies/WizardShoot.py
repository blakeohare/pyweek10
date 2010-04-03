
class WizardShoot(Sprite):
	
	def __init__(self, x, y, vx, vy):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 16
		self.height = 16
		self._vx = vx
		self._vy = vy
		self.immune_to_gravity = True
		self.moves_through_walls = True
		self.invincible = True
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		if self.lifetime > 60 and int(self.lifetime % 2) == 0:
			return
		
		num = int(self.lifetime % 3)
		
		img = images.Get('wands/left/shoot_fire'+str(num)+'.png')
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		self.x += self._vx
		self.y += self._vy
		
		if self.lifetime > 90:
			self.expired = True
			
		