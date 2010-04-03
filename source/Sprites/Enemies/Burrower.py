
class EnemyBurrow(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 20
		self.height = 15
		self.left_facing = True
		self.state_counter = int((7 * x / 16.0) % 60)
		self.state = ('burrowed','out')[int((x / 16.0) % 2) == 0]
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('Right', 'Left')[self.left_facing]
		
		num = 1
		
		if self.state == 'rising' or self.state == 'burrowing':
			num = max(0, min(int(self.state_counter / 4), 2))
			if self.state == 'burrowing':
				num = 2 - num
			num += 2
		elif self.state == 'out':
			num = 4
		elif self.state == 'shoot':
			num = 5
		
		
		
		file = direction + str(num) + '.png'
		
		img = images.Get('sprites/Enemies/Burrower/' + file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		self.state_counter += 1
		
		self.left_facing = playScene.player.x < self.x
		
		if self.state == 'burrowed':
			if self.state_counter == 60:
				self.state_counter = 0
				self.state = 'rising'
		elif self.state == 'rising':
			if self.state_counter == 12:
				self.state_counter = 0
				self.state = 'out'
		
		elif self.state == 'burrowing':
			if self.state_counter == 12:
				self.state_counter = 0
				self.state = 'burrowed'
		
		elif self.state == 'out':
			if self.state_counter == 60:
				self.state_counter = 0
				self.state = 'shoot'
		
		elif self.state == 'shoot':
			if self.state_counter == 3:
				playScene.enemies.append(EnemyBurrowerBullet(self.x, self.y + 4, (2,-2)[self.left_facing]))
				
			if self.state_counter == 20:
				self.state_counter = 0
				self.state = 'burrowing'
			
		