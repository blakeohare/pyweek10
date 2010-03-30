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
		
class Level:
	def __init__(self, level_template):
		self.level_template = level_template
	
	def get_tile(self, col, row):
		return self.level_template.get_tile(col, row)
	
	def get_width(self):
		return self.level_template.get_width()
	
	def get_height(self):
		return self.level_template.get_height()
	
	def get_victory_x(self):
		return self.level_template.values['victoryX']
		
	def get_landing_platforms_in_rectangle(self, x_start, x_end, y_start, y_end):
		#perf is important here, note that this code is duplicated in the other methods
		x_start = max(0, x_start)
		x_end = min(x_end, self.get_width() - 1)
		y_start = max(0, y_start)
		y_end = min(y_end, self.get_height() - 1)
		
		landing = []
		
		tiles = self.level_template.tiles
		width = self.level_template.width
		
		x = x_start
		while x <= x_end:
			y = y_start
			while y <= y_end:
				p = tiles[y * width + x].get_platforms()
				landing += p['solid']
				landing += p['jumpthrough']
				landing += p['blocking']
				landing += p['inclines']
				y += 1
			x += 1
		return landing
	
	def get_walls_in_rectangle(self, x_start, x_end, y_start, y_end):
		#perf is important here, note that this code is duplicated in the other methods
		x_start = max(0, x_start)
		x_end = min(x_end, self.get_width() - 1)
		y_start = max(0, y_start)
		y_end = min(y_end, self.get_height() - 1)
		
		landing = []
		
		tiles = self.level_template.tiles
		width = self.level_template.width
		
		x = x_start
		while x <= x_end:
			y = y_start
			while y <= y_end:
				p = tiles[y * width + x].get_platforms()
				landing += p['solid']
				y += 1
			x += 1
		
		return landing
	
	def get_ceilings_in_rectangle(self, x_start, x_end, y_start, y_end):
		#perf is important here, note that this code is duplicated in the other methods
		x_start = max(0, x_start)
		x_end = min(x_end, self.get_width() - 1)
		y_start = max(0, y_start)
		y_end = min(y_end, self.get_height() - 1)
		
		landing = []
		
		tiles = self.level_template.tiles
		width = self.level_template.width
		
		x = x_start
		while x <= x_end:
			y = y_start
			while y <= y_end:
				p = tiles[y * width + x].get_platforms()
				landing += p['blocking']
				landing += p['solid']
				y += 1
			x += 1
		
		return landing
		
	def get_inclines_in_rectangle(self, x_start, x_end, y_start, y_end):
		#perf is important here, note that this code is duplicated in the other methods
		x_start = max(0, x_start)
		x_end = min(x_end, self.get_width() - 1)
		y_start = max(0, y_start)
		y_end = min(y_end, self.get_height() - 1)
		
		landing = []
		
		tiles = self.level_template.tiles
		width = self.level_template.width
		
		x = x_start
		while x <= x_end:
			y = y_start
			while y <= y_end:
				p = tiles[y * width + x].get_platforms()
				landing += p['inclines']
				y += 1
			x += 1
		
		return landing
	
	
class LevelTemplate:
	def __init__(self, tiles, width, values):
		self.width = width
		self.tiles = tiles
		self.values = values
		self.height = int(len(self.tiles) / width)
		
		default_values = {
			'victoryX' : 0
		}
		
		for key in default_values.keys():
			if not (key in self.values.keys()):
				self.values[key] = default_values['victoryX']
	
	def get_tile(self, col, row):
		return self.tiles[self.width * row + col]
	
	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height
		
#STATIC
levels = LevelLibrary()