class ConfigureControlsScene:
	def __init__(self):
		self.next = self
		self.counter = 0
		self.index = 0
	
	def Update(self):
		self.counter += 1
	
	def ProcessInput(self, events):
		sources = input.get_input_sources()[1:]
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
						
	
	def writeText(self, text, indent = True):
		screen = self.screen
		x = (30, 60)[indent]
		screen.blit(get_text(text), (x, self.line_next))
		
		self.line_next += 18
	def Render(self, screen):
		self.screen = screen
		title = get_text('Input Configuration')
		self.line_next = 30
		screen.blit(title, (128 - int(title.get_width() / 2.0), 10))
		
		
		
		self.writeText('Keyboard Controls:', False)
		self.writeText('Arrow Keys: Move')
		self.writeText('Space: Jump')
		self.writeText('Z: Shoot Wand')
		self.writeText('X: Run')
		self.writeText('Enter: Pause')
		
		no_joysticks = len(input.get_input_sources()) == 1
		
		
		
		if no_joysticks:
			self.writeText("For maximum enjoyment, plug in", False)
			self.writeText("a USB controller or joystick", False)
			self.writeText('and relaunch the game!', False)
			self.writeText('')
		else:
			self.writeText('Enable Joystick:', False)
		
		i = 0
		for input_source in input.get_input_sources()[1:]:
			active = ''
			if input_source == input.get_active_joystick():
				active = '(ACTIVE) '
			if self.index == i:
				screen.blit(images.Get('title_cursor.png'), (38, self.line_next))
			self.writeText(active + input_source.get_name())
			
			i += 1
		
		#if no_joysticks:
		#	self.writeText("No Joysticks Plugged In")
		
		if self.index == i:
			screen.blit(images.Get('title_cursor.png'), (38, self.line_next))
		self.writeText('Exit Configuration')
		
		
	