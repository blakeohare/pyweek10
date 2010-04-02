class JoystickConfig:
	def __init__(self, previous_menu, joystick):
		self.previous_menu = previous_menu
		self.next = self
		self.counter = 0
		self.joystick = joystick #JoystickInputSource instance
		self.keys = 'up right down left start A B Y L R'.split(' ')
		self.descriptions = {
			'up' : "Press the button for UP",
			'down' : "Press the button for DOWN",
			'left' : "Press the button for LEFT",
			'right' : "Press the button for RIGHT",
			'start' : "Press the button for START/PAUSE",
			'A' : "Press the button for RUN",
			'B' : "Press the button for JUMP",
			'Y' : "Press the button for ATTACK",
			'X' : "Press the button for MAP",
			'L' : "Press the left trigger",
			'R' : "Press the right trigger"
		}
		
		self.config_index = 0
		self.joystick.reset_mappings()
		self.down_pressed = False
		self.keys_released = False
		
	def Update(self):
		self.counter += 1
		
		if self.config_index == 0 and not self.keys_released:
			# When entering the menu by pressing the joystick, it will use the
			# button you pressed to enter the menu as the first configuration value.
			# This will wait for the keys to ALL be released before listening to any value.
			if not self.joystick.any_keys_pressed():
				self.keys_released = True
		elif self.config_index < len(self.keys):
			key = self.keys[self.config_index]
			if self.joystick.configure_key(key):
				self.config_index += 1
		else:
			input.set_active_joystick(self.joystick)
			
	
	def ProcessInput(self, events):
		if self.config_index >= len(self.keys):
			for event in events:
				if event.key == 'start':
					if event.down:
						self.down_pressed = True
					elif self.down_pressed:
						self.previous_menu.next = self.previous_menu
						self.next = self.previous_menu
	
	def Render(self, screen):
		img = images.Get('joystick_config/joystick_basic.png')
		
		if self.config_index < len(self.keys):
			key = self.keys[self.config_index]
			texts = [self.descriptions[key]]
			if int(self.counter / 10) % 2 == 0:
				img = images.Get('joystick_config/joystick_' + key.lower() + '.png')
		else:
			texts = ["Configuration complete", "Press START or ENTER"]
		y = 10
		for text in texts:
			screen.blit(get_text(text), (10, y))
			y += 12
		screen.blit(img, (40, 40))
		