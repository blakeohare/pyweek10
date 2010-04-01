class PlaySceneInfoScene:
	
	def __init__(self, world, level):
		
		self.next = self
		self.world = str(world)
		self.level = str(level)
		self.counter = 0
		self.duration = 10 #TODO: change this to 60 before release
		
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		self.counter += 1
		
		if (self.counter == self.duration):
			level_id = self.world + '_' + self.level
			playScene = PlayScreen(level_id, 'a')
			self.next = TransitionScene(self, playScene, 'fade_then_circle', 50)
	
	def Render(self, screen):
		
		screen.fill((0,0,0))
		
		text = get_text("Level " + self.world + " - " + self.level)
		x = 128 - int(text.get_width() / 2)
		y = 80 - int(text.get_height() / 2)
		screen.blit(text, (x, y))
		