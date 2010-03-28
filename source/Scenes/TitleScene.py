class TitleScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
	
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'start':
				self.next = SelectGameScene()
			elif event.key == 'L':
				self.next = CutSceneScene()
	
	def Render(self, screen):
		screen.blit(images.Get('title.png'), (0, 0))
	
	def Update(self):
		self.counter += 1