
class EnemyCornelius(Sprite):
	
	def __init__(self, x, y):
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.width = 19
		self.height = 25
		self.left_facing = True
		self.next_jump = 30
		self.hp = 25
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('right', 'left')[self.left_facing]
		
		num = int((self.lifetime / 3.0)% 3)
		
		file = direction + str(num) + '.png'
		
		img = images.Get('sprites/EvilWizardDude/' + file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	def GetPowerUp(self, counter, playScene):
		#terrible hackery
		playScene.next = CutSceneScene('endgame', CreditsScene())
	
	def update(self, playScene):
		self.lifetime += 1
		
		self.left_facing = True
		
		if self.lifetime == self.next_jump:
			self.next_jump += random.choice((30, 60, 50))
			self.platform = None
			self.on_ground = False
			self.vy = -10
		
		if int(self.lifetime % 20.0) == 19:
			
			dy = self.y - playScene.player.y
			dx = abs(self.x - playScene.player.x) + 0.0
			
			vx = -3.0
			
			if dx == 0: dx = .1
			
			vy = vx * dy / dx
			
			playScene.enemies.append(WizardShoot(self.x, self.y, int(vx), int(vy)))
		