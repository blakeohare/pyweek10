
class MainCharacter(Sprite):
	
	def __init__(self, x, y):
		Sprite.__init__(self, x, y)
		self.width = 14
		self.height = 30
		self.flashing_counter = 0
		self.special_state = None
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		if self.flashing_counter > 0 and (self.flashing_counter & 1) == 1:
			return
		
		direction = ('right', 'left')[self.left_facing]
		
		if self.special_state != None:
			img = self.special_state.draw(surface, self, is_moving, counter)
		else:
			if self.vy > 0:
				file = direction + 'jump2'
			elif self.vy < 0:
				file = direction + 'jump1'
			elif is_moving:
				file = direction + 'walk' + str(int(int(counter / 3) % 3))
			else:
				file = direction + 'stand'
			file += '.png'
			
			img = images.Get('sprites/ClumsyWizard/' + file)
		
		xy = self.get_top_left()
		img_offset = images.GetOffset(img)
		x = xy[0] - camera_offset[0] + img_offset[0]
		y = xy[1] - camera_offset[1] + img_offset[1]
		
		surface.blit(img, (x, y))
	
	def update(self, playScene):
		self.flashing_counter -= 1
		if self.special_state != None:
			self.special_state.update(self, playScene)
			if self.special_state.expires <= 0:
				self.special_state = None
