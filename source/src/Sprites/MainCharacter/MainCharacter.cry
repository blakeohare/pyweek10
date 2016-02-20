
class MainCharacter(Sprite):
	
	def __init__(self, x, y):
		Sprite.__init__(self, x, y)
		self.width = 14
		self.height = 30
		self.flashing_counter = 0
		self.special_state = None
		self.confined_to_scene = True
		self.wand_cooldown = 0
		self.holding_ladder = False
		self.was_holding_ladder = False
		self.prev_loc = (x, y)
		self.ladder_climb = False
		self.ladder_images = '1 1 1 1 2 2 2 2'.split(' ')
		self.lifetime = 0
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		if self.flashing_counter > 0 and (self.flashing_counter & 1) == 1:
			return
		
		direction = ('right', 'left')[self.left_facing]
		
		if self.special_state != None:
			img = self.special_state.draw(surface, self, is_moving, counter)
		elif self.wand_cooldown > 0:
			img = images.Get('sprites/ClumsyWizard/' + direction + 'throw' + ('1','2')[self.wand_cooldown > 2] + '.png')
		elif self.holding_ladder:
			if self.ladder_climb:
				self.ladder_images = self.ladder_images[1:] + [self.ladder_images[0]]
			img = images.Get('sprites/ClumsyWizard/climb'+self.ladder_images[0]+'.png') #TODO: climb 2
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
		self.lifetime += 1
		self.prev_loc = (self.x, self.y)
		
		self.flashing_counter -= 1
		if self.special_state != None:
			self.special_state.update(self, playScene)
			if self.special_state.expires <= 0:
				self.special_state = None
