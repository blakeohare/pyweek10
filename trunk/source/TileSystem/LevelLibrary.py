class LevelLibrary:
	
	def __init__(self):
		self.levels = {}
	
	def get_level(self, level_key):
		if not (level_key in self.levels.keys()):
			self.load_level(level_key)
		return Level(self.levels[level_key])
	
	def load_level(self, level_key):
		file = os.path.join('levels', 'levels', level_key + '.txt')
		c = open(file, 'rt')
		lines = trim(c.read()).split('\n')
		c.close()
		
		values = {}
		width = 0
		victory = -1
		tile_keys = []
		start_locations = None
		default_start = None
		doors = []
		background = None
		background_scroll = 0
		enemies = []
		storm = False
		for line in lines:
			line = trim(line)
			if len(line) > 0:
				line = line.split(':')
				item = line[0]
				line = ':'.join(line[1:])
				if item == 'width':
					width = int(line)
				elif item == 'tiles':
					tile_keys = line.split(' ')
				#elif item == 'victoryX':
				#	values['victoryX'] = int(line)
				elif item == 'default_start':
					values['default_start'] = line
				elif item == 'start_locations':
					start_locations = line
				elif item == 'background_image':
					if line == 'stormy1':
						storm = True
					background = images.Get('backgrounds/' + line + '.png')
				elif item == 'background_scroll_rate':
					background_scroll = float(line)
				elif item == 'doors':
					if line != '':
						for door in line.split(' '):
							parts = door.split('|')
							coords = parts[0].split(',')
							dest = parts[1].split(',')
							doors.append((int(coords[0]), int(coords[1]), dest[0], dest[1]))
				elif item == 'enemies':
					if line != '':
						for enemy in line.split(' '):
							parts = enemy.split(',')
							enemy_type = parts[0]
							x = int(parts[1])
							y = int(parts[2])
							enemies.append((enemy_type, x, y))
		
		values['enemies'] = enemies
		values['storm'] = storm
		values['doors'] = doors
		values['start_locations'] = {}
		values['background'] = background
		values['background_scroll'] = background_scroll
		for loc in start_locations.split(' '):
			parts = loc.split(',')
			values['start_locations'][parts[0]] = (int(parts[1]), int(parts[2]))

		tiles = []
		x = 0
		y = 0
		
		victory_found = False
		
		previous_is_up_incline = False
		for tile_key in tile_keys:
			keys = tile_key.split(',')
			if len(keys) == 1:
				tiles.append(tile_library.GetTile(x * 16, y * 16, keys[0]))
			else:
				tiles.append(tile_library.GetCompositeTile(x * 16, y * 16, keys))
			
			is_victory = False
			
			for key in keys:
				if key == 'b2' and not victory_found:
					is_victory = True
					values['victoryX'] = x * 16 + 8
					victory_found = True
			
			if len(tiles) > 1 and tiles[-1].has_down_inclines():
				tiles[-2].remove_walls(False)
				previous_is_up_incline = False
			elif tiles[-1].has_up_inclines():
				previous_is_up_incline = True
			elif previous_is_up_incline:
				tiles[-1].remove_walls(True)
				previous_is_up_incline = False
			else:
				previous_is_up_incline = False
			
			x += 1
			if x == width:
				x = 0
				y += 1
		
		
		self.levels[level_key] = LevelTemplate(tiles, width, values)
		self.levels[level_key]._remove_me = level_key #TODO: remove me
		
#STATIC
levels = LevelLibrary()