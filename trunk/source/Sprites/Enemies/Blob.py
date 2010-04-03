
class EnemyBlob(Sprite):
	
	def __init__(self, x, y, color='green'):
		self.lifetime = int(int(7 * x / 16.0) % 100)
		Sprite.__init__(self, x, y)
		self.width = 16
		self.height = 16
		self.left_facing = True
		self.state = 'waiting'
		self.color = color
		self.image_folder = color + ' Blob'
		self.image_folder = self.image_folder[0].upper() + self.image_folder[1:]
		self.state_counter = self.lifetime
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('right', 'left')[self.left_facing]
		
		file = direction + str(int(int(counter / 5) % 3)) + '.png'
		
		img = images.Get('sprites/Enemies/'+self.image_folder+'/' + file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.lifetime += 1
		self.state_counter += 1
		self.left_facing = playScene.player.x < self.x
		walk_duration = 30
		velocity = 1
		if self.color == 'blue':
			walk_duration = 60
		if self.color == 'red':
			walk_duration = 90
			velocity = 2
		if self.state == 'waiting':
			self.vx = 0
			if self.state_counter >= 60:
				self.state_counter = 0
				self.state = 'walking'
		elif self.state == 'walking':
			self.vx = (velocity, -velocity)[self.left_facing]
			if self.color != 'green' and self.is_going_to_vx_bad(playScene):
				self.vx = 0
			if self.state_counter > walk_duration:
				self.state_counter = 0
				self.state = 'waiting'
		
		