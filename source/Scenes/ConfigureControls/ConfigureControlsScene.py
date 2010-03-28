class ConfigureControlsScene:
	def __init__(self):
		self.next = self
		self.counter = 0
		self.index = 0
	
	def Update(self):
		self.counter += 1
	
	def ProcessInput(self, events):
		sources = input.get_input_sources()
		for event in events:
			if event.down:
				if event.key == 'up':
					self.index = max(0, self.index - 1)
				elif event.key == 'down':
					self.index = min(len(sources), self.index + 1)
				elif event.key in ('start', 'A', 'B'):
					if len(sources) > self.index:
						source = sources[self.index]
						if source.get_input_type() == 'keyboard':
							self.next = KeyboardConfig(self)
						elif source.get_input_type() == 'joystick':
							self.next = JoystickConfig(self, source)
					else: #last item is "exit"
						self.next = TitleScene()
						
	
	def Render(self, screen):
		screen.blit(get_text('INPUT CONFIGURATION'), (60, 10))

		y = 30
		x = 60
		i = 0
		for input_source in input.get_input_sources():
			active = ''
			if input_source == input.get_active_joystick():
				active = ' -- ACTIVE'
			screen.blit(get_text(input_source.get_name() + active), (x, y))
			if self.index == i:
				screen.blit(images.Get('title_cursor.png'), (x - 12, y))
			y += 15
			i += 1
		
		y += 10
		
		screen.blit(get_text('EXIT'), (x, y))
		if self.index == i:
			screen.blit(images.Get('title_cursor.png'), (x - 12, y))
		
		
	