
class InputModel:
	def __init__(self):
		self.keys = {
			'up' : False,
			'down' : False,
			'left' : False,
			'right' : False,
			'A' : False,
			'B' : False,
			'X' : False,
			'Y' : False,
			'start' : False,
			'L' : False,
			'R' : False
			}
		self.keyboard = KeyboardInputSource()
		self.joysticks = []
		self.active_joystick = None
		
		#TODO: set automated input to overtake KeyboardInputSource for automated gameplay cutscenes
	
	def add_joystick(self, joystick):
		self.joysticks.append(JoystickInputSource(joystick))
	
	def set_active_joystick(self, joystick):
		self.active_joystick = joystick
	
	def get_input_sources(self):
		return [self.keyboard] + self.joysticks
	
	def get_active_input_sources(self):
		if self.active_joystick == None:
			return [self.keyboard]
		return [self.keyboard, self.active_joystick]
	
	def get_active_joystick(self):
		return self.active_joystick
	
	def get_input(self, pygame_events):
		inputevents = []
		for source in self.get_active_input_sources():
			inputevents += source.process_events(pygame_events)
			for event in inputevents:
				self.keys[event.key] = event.down
				
		return inputevents
	
	def is_key_pressed(self, key):
		return self.keys[key]
	
#STATIC

input = InputModel()