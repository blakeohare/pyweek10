
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
		self.sources = [KeyboardInputSource()]
		
		#TODO: detect joysticks
		#TODO: set automated input to overtake KeyboardInputSource for automated gameplay cutscenes
	
	def get_input(self, pygame_events):
		inputevents = []
		for source in self.sources:
			inputevents += source.process_events(pygame_events)
			for event in inputevents:
				self.keys[event.key] = event.down
				
		return inputevents
	
	def is_key_pressed(self, key):
		return self.keys[key]

#STATIC

input = InputModel()