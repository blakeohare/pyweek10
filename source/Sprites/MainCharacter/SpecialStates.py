
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
			parts = playScene.level_id.split('_')
			world = int(parts[0])
			level = parts[1][0] #TODO: make this robust if we ever have more than 9 levels in each
			playScene.next = TransitionScene(playScene, MapScene(world, level), 'circle_in', 59, (x, y))

class SpecialStateVictory:
	def __init__(self, player, mapScene):
		self.lifetime = 0
		self.expires = 100
		self.player = player
		self.x = player.x
		self.y = player.y
		self.block_update = True
		self.mapScene = mapScene
		
	def draw(self, surface, main_char, is_moving, counter):
		sequence = ['rightstand','rightwalk0','rightturn1','rightturn2','rightturn3','leftturn3','leftturn2','leftturn1','leftwalk0','leftstand', 'wave1']
		if self.lifetime > 10 and self.lifetime <= 29:
			index = int((self.lifetime - 10) / 2)
		elif self.lifetime <= 10:
			index = 0
		else:
			index = -1
			
		return images.Get('sprites/ClumsyWizard/' + sequence[index] + '.png')
	
	def update(self, main_char, playScene):
		self.expires -= 1
		self.lifetime += 1
		if self.expires == 60:
			camera = playScene.get_camera_offset()
			x = self.x - camera[0]
			y = self.y - camera[1]
			playScene.next = TransitionScene(playScene, self.mapScene, 'circle_in', 50, (x, y))