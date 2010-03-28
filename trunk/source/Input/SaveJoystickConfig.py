
def save_joystick_config():
	joystick = input.get_active_joystick()
	joystick_file = ''
	if joystick != None:
		keys = joystick.keys
		name = joystick.get_name()
		joystick_file = name
		for key in keys:
			joystick_file += "\n" + key + ':'
			mapping = joystick.mapping[key]
			if mapping[0] == 'button':
				joystick_file += 'button ' + str(mapping[1])
			elif mapping[0] == 'hat':
				joystick_file += 'hat ' + str(mapping[1]) + ' ' + str(mapping[2][0]) + ' ' + str(mapping[2][1])
			elif mapping[0] == 'axis':
				joystick_file += 'axis ' + str(mapping[1]) + ' ' + str(mapping[2])
			
	c = open(os.path.join('saved', 'joystick.txt'), 'wt')
	c.write(joystick_file)
	c.close()
	
def load_joystick_config():
	file = os.path.join('saved', 'joystick.txt')
	if os.path.exists(file):
		c = open(file, 'rt')
		lines = trim(c.read()).split('\n')
		c.close()
		name = ''
		mapping = {}
		keys = 'up down left right start A B X Y L R'.split(' ')
		
		for key in keys:
			mapping[key] = ('none')
		
		for line in lines:
			line = trim(line)
			if name == '':
				name = line
			else:
				parts = line.split(':')
				if len(parts) == 2:
					key = parts[0]
					if key in keys:
						parts = parts[1].split(' ')
						type = parts[0]
						if type == 'button' and len(parts) == 2:
							button = int(parts[1])
							mapping[key] = ('button', button)
						elif type == 'hat' and len(parts) == 4:
							hat = int(parts[1])
							x = int(parts[2])
							y = int(parts[3])
							mapping[key] = ('hat', hat, (x, y))
						elif type == 'axis' and len(parts) == 3:
							axis = int(parts[1])
							value = int(parts[2])
							mapping[key] = ('axis', axis, value)
		
		for joystick in input.get_joysticks():
			if joystick.get_name() == name:
				joystick.mapping = mapping
				input.set_active_joystick(joystick)
				return
				