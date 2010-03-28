class SavedGame:
	
	def __init__(self, slot_num):
		self.path = 'saved' + os.sep + 'slot_' + str(slot_num) + '.txt'
		self.slot = slot_num
		
		if os.path.exists(self.path):
			self.values = self.read_slot_file(self.path)
		else:
			self.values = {
			'name' : '',
			'saved' : 0
			}
	
	def read_slot_file(self, path):
		c = open(path, 'rt')
		lines = c.read().split('\n')
		c.close()
		
		values = {}
		for line in lines:
			line = trim(line)
			
			if line != '':
				is_int = line[0] == '#'
				if is_int:
					line = line[1:]
				parts = line.split(':')
				key = parts[0]
				value = ':'.join(parts[1:])
				if is_int:
					value = int(value)
				values[key] = value
		return values

	def save_to_file(self):
		output = []
		for key in self.values.keys():
			name = key
			value = self.values[key]
			if type(value) == type(1):
				name = "#" + name
				value = str(value)
			
			output.append(name + ':' + value)
		
		c = open(self.path, 'wt')
		c.write('\n'.join(output))
		c.close()
	
	def save_value(self, name, value):
		self.values[name] = value
	
	def get_value(self, name):
		return self.values[name]

class SavedState:
	def __init__(self):
		self.active_saved_game = None
		self.saved_games = []
		
		for slot_num in (1, 2, 3):
			self.saved_games.append(SavedGame(slot_num))
	
	def active_game(self):
		return self.active_saved_game
	
	def set_active_game(self, slot_num):
		self.active_saved_game = self.saved_games[slot_num - 1]
	
	def get_saved_game(self, slot_num):
		return self.saved_games[slot_num - 1]
	
	def erase_game(self, slot_num):
		game = self.get_saved_game(slot_num)
		if game.get_value('saved') == 1:
			proxy_game = SavedGame(4) # does not exist
			game.values = proxy_game.values
			game.save_to_file()
	
	def copy_game(self, slot_from, slot_to):
		game_from = self.get_saved_game(slot_from)
		game_to = self.get_saved_game(slot_to)
		game_to.values = game_from.values
		game_to.save_to_file()
		
		# now it's a reference to the same dictionary instance but the files are correct
		# clear instance and re-instantiate one so the dictionary instances are unique
		
		self.saved_games[slot_to - 1] = SavedGame(slot_to)
		
		

#STATIC
games = SavedState()