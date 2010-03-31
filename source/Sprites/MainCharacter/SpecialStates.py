
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

			