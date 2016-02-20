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
					elif self.index == 1:
						self.next = ConfigureControlsScene()
					else:
						self.next = TransitionScene(self, None, 'fade_and_end', 30)
					
				elif event.key == 'up':
					self.index = max(0, self.index - 1)
				elif event.key == 'down':
					self.index = min(2, self.index + 1)
	
	def Render(self, screen):
		screen.blit(images.Get('title.png'), (0, 0))
		screen.blit(get_text('Start'), (60, 150))
		screen.blit(get_text('Keyboard Controls/Joystick'), (60, 170))
		screen.blit(get_text('Exit'), (60, 190))
		screen.blit(images.Get('title_cursor.png'), (48, 152 + self.index * 20))
	
	def Update(self):
		self.counter += 1
		if self.counter == 1:
			jukebox.PlayTitle()