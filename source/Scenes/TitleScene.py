class TitleScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
		self.index = 0
		
	def ProcessInput(self, events):
		for event in events:
			if event.down:
				if event.key in ('start', 'A', 'B'):
					if self.index == 0:
						self.next = SelectGameScene()
					else:
						self.next = ConfigureControlsScene()
				elif event.key == 'L':
					self.next = CutSceneScene('demo')
					
				elif event.key == 'up':
					self.index = max(0, self.index - 1)
				elif event.key == 'down':
					self.index = min(1, self.index + 1)
	
	def Render(self, screen):
		screen.blit(images.Get('title.png'), (0, 0))
		screen.blit(get_text('START'), (60, 160))
		screen.blit(get_text('CONFIGURE CONTROLS'), (60, 180))
		screen.blit(images.Get('title_cursor.png'), (48, 160 + self.index * 20))
	
	def Update(self):
		self.counter += 1
		if self.counter == 1:
			jukebox.PlayTitle()