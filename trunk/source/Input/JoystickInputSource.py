
class JoystickInputSource:
	def __init__(self, pygame_joystick):
		self.joystick = pygame_joystick
		self.keys = 'up down left right start A B X Y L R'.split(' ')
		self.reset_mappings()
		
	def reset_mappings(self):
		self.mapping = {}
		self.current_state = {}
		
		for key in self.keys:
			self.mapping[key] = ('none')
			self.current_state[key] = False
		
	def get_input_type(self):
		return 'joystick'
	
	def get_id(self):
		return self.joystick.get_id()
	
	def get_name(self):
		return self.joystick.get_name()
	
	def any_keys_pressed(self):
		for hat in range(self.joystick.get_numhats()):
			if not (self.joystick.get_hat(hat) == (0,0)):
				return True
		
		for button in range(self.joystick.get_numbuttons()):
			if self.joystick.get_button(button):
				return True
		
		for axis in range(self.joystick.get_numaxes()):
			if abs(self.joystick.get_axis(axis)) > 0.3:
				return True
		
		return False
	
	def is_key_pressed(self, key):
		mapping = self.mapping[key]
		if mapping[0] == 'none':
			return False
		
		if mapping[0] == 'button':
			button_id = mapping[1]
			return self.joystick.get_button(button_id)
		
		if mapping[0] == 'hat':
			hat_id = mapping[1]
			map_vector = mapping[2]
			actual_vector = self.joystick.get_hat(hat_id)
			
			if map_vector[0] != 0:
				return map_vector[0] == actual_vector[0]
			else:
				return map_vector[1] == actual_vector[1]
		
		if mapping[0] == 'axis':
			axis_id = mapping[1]
			value = self.joystick.get_axis(axis_id)
			if value > 0.3: value = 1
			elif value < -0.3: value = -1
			else: value = 0
			return value == mapping[2]
		
		return False #this should never happen
				
	
	def process_events(self, pygame_events):
		events = []
		for key in self.keys:
			state = self.is_key_pressed(key)
			if state != self.current_state[key]:
				events.append(InputEvent(key, state))
				self.current_state[key] = state
		return events
	
	def mapping_doesnt_exist_already(self, mapping):
		for value in self.mapping.values():
			if value == mapping: return False
		return True
	
	def configure_key(self, key):
		for button_id in range(self.joystick.get_numbuttons()):
			if self.joystick.get_button(button_id):
				value = ('button', button_id)
				if self.mapping_doesnt_exist_already(value):
					self.mapping[key] = value
					return True
		
		for hat_id in range(self.joystick.get_numhats()):
			vector = self.joystick.get_hat(hat_id)
			if vector[0] != 0:
				value = ('hat', hat_id, (vector[0], 0))
				if self.mapping_doesnt_exist_already(value):
					self.mapping[key] = value
					return True
			elif vector[1] != 0:
				value = ('hat', hat_id, (0, vector[1]))
				if self.mapping_doesnt_exist_already(value):
					self.mapping[key] = value
					return True
		
		for axis_id in range(self.joystick.get_numaxes()):
			value = self.joystick.get_axis(axis_id)
			if value > 0.3:
				value = ('axis', axis_id, 1)
				if self.mapping_doesnt_exist_already(value):
					self.mapping[key] = value
					return True
			elif value < -0.3:
				value = ('axis', axis_id, -1)
				if self.mapping_doesnt_exist_already(value):
					self.mapping[key] = value
					return True
		
		return False # no key was found