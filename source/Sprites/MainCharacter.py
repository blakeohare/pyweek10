
#TODO: split this into a parent sprite class when it comes time to make other enemies

class MainCharacter:
	
	def __init__(self, x, y):
		self.x = x # these points are the CENTER of the player
		self.y = y
		self.vy = 0
		self.vx = 0
		self.dx = 0
		self.dy = 0
		self.width = 14
		self.height = 30
		self.on_ground = False
		self.platform = None
		self.left_facing = False
		self.special_state = None
	
	def get_top_left(self):
		return (self.get_left(), self.get_top())
	
	def get_left(self):
		return int(self.x - self.width / 2)
	
	def get_top(self):
		return int(self.y - self.height / 2)
	
	def get_head_bonk_top(self):
		return int(self.y - self.height / 2) + 5
	
	def get_bottom(self):
		return self.get_top_left()[1] + self.height
	
	def get_left(self):
		return int(self.x - self.width / 2)
	
	def get_right(self):
		return self.get_left() + self.width
		
	def draw(self, surface, is_moving, counter, camera_offset):
		
		direction = ('right', 'left')[self.left_facing]
		
		if self.special_state != None:
			img = self.special_state.draw(surface, self, is_moving, counter)
		else:
			if is_moving:
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
		if self.special_state != None:
			self.special_state.update(self, playScene)
			if self.special_state.expires <= 0:
				self.special_state = None

#Special States
class SpecialStateDoorEntry:
	def __init__(self, door, player):
		self.expires = 10
		self.player = player
		self.door = door
		self.direction = ('right', 'left')[player.left_facing]
		self.block_update = True
	
	def draw(self, surface, main_char, is_moving, counter):
		file = 'sprites/ClumsyWizard/' + self.direction + 'stand.png'
		return images.Get(file)
		
	def update(self, main_char, playScene):
		self.expires -= 1
		if self.expires <= 0:
			playScene.next = TransitionScene(playScene, PlayScreen(playScene.level_id, self.door[0], self.door[1]), 'fadeout', 20)
			
class SpecialStateDying:
	def __init__(self, player):
		self.expires = 120
		self.player = player
		self.x = self.player.x
		self.y = self.player.y + 7
		self.block_update = True
	
	def draw(self, surface, main_char, is_moving, counter):
		return images.Get('sprites/ClumsyWizard/sleeping.png')
	
	def update(self, main_char, playScene):
		self.expires -= 1
		if self.expires == 60:
			camera = playScene.get_camera_offset()
			x = self.x - camera[0]
			y = self.y - camera[1]
			playScene.next = TransitionScene(playScene, MapScene(int(playScene.level_id.split('_')[0])), 'circle_in', 59, (x, y))

			