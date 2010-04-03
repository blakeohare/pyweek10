
class EnemyThingy(Sprite):
	
	def __init__(self, x, y, color='earth'):
		self.lifetime = int(int(7 * x / 16.0) % 100)
		Sprite.__init__(self, x, y)
		self.width = 19
		self.height = 15
		self.left_facing = True
		self.state = 'waiting'
		self.color = color
		self.image_folder = color + ' Thingy'
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

	def jump(self):
		self.vy = -8
		self.platform = None
		self.on_ground = False
		
	def update(self, playScene):
		self.lifetime += 1
		self.state_counter += 1
		self.left_facing = playScene.player.x < self.x
		walk_duration = 30
		velocity = 1
		if self.color == 'frost':
			walk_duration = 60
		if self.color == 'flare':
			walk_duration = 90
			velocity = 2
		if self.state == 'waiting':
			self.vx = 0
			if self.state_counter >= 20:
				self.state_counter = 0
				self.jump()
				self.state = 'walking'
		elif self.state == 'walking':
			self.vx = (velocity, -velocity)[self.left_facing]
			if self.color != 'earth' and self.is_going_to_vx_bad(playScene):
				self.vx = 0
			elif int(self.state_counter % 40.0) == 39:
				self.jump()
			
			if self.state_counter > walk_duration:
				self.state_counter = 0
				self.state = 'waiting'
			
			
		
		