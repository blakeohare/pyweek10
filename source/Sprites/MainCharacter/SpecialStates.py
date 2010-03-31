
class SpecialStateDoorEntry:
	def __init__(self, door, player):
		self.expires = 60
		self.player = player
		self.lifetime = 0
		self.door = door
		self.direction = ('right', 'left')[player.left_facing]
		self.block_update = True
	
	def draw(self, surface, main_char, is_moving, counter):
		num = 1
		if self.lifetime > 3:
			num = 2
		if self.lifetime > 6:
			num = 3
			
		file = 'sprites/ClumsyWizard/' + self.direction + 'turn' + str(num) + '.png'
		return images.Get(file)
		
	def update(self, main_char, playScene):
		self.lifetime += 1
		self.expires -= 1
		if self.lifetime == 7:
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

			