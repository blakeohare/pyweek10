
class KeyboardInputSource:
	def __init__(self):
		self.keymap = {
			K_UP : 'up',
			K_DOWN : 'down',
			K_LEFT : 'left',
			K_RIGHT : 'right',
			K_SPACE : 'B',
			K_z : 'Y',
			K_x : 'A',
			K_m : 'X',
			K_RETURN : 'start',
			K_1 : 'L',
			K_2 : 'R'
			}
	
	def process_events(self, pygame_events):
		events = []
		for event in pygame_events:
			if event.type == KEYDOWN or event.type == KEYUP:
				if event.key in self.keymap.keys():
					events.append(InputEvent(self.keymap[event.key], event.type == KEYDOWN))
		return events
		