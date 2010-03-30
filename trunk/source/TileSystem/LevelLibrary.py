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
				elif item == 'victoryX':
					values['victoryX'] = int(line)
				elif item == 'default_start':
					values['default_start'] = line
				elif item == 'start_locations':
					start_locations = line
				elif item == 'background_image':
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
		for tile_key in tile_keys:
			keys = tile_key.split(',')
			if len(keys) == 1:
				tiles.append(tile_library.GetTile(x * 16, y * 16, keys[0]))
			else:
				tiles.append(tile_library.GetCompositeTile(x * 16, y * 16, keys))
			x += 1
			if x == width:
				x = 0
				y += 1
		
		self.levels[level_key] = LevelTemplate(tiles, width, values)
		
#STATIC
levels = LevelLibrary()