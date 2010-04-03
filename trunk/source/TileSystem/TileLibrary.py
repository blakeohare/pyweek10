class TileLibrary:
	
	def __init__(self):
		
		self.tiles = {}
		
		for file in os.listdir('tiles'):
			if file.endswith('.txt'):
				path = os.path.join('tiles', file)
				c = open(path, 'rt')
				lines = trim(c.read()).split('\n')
				c.close()
				for line in lines:
					line = trim(line)
					if len(line) > 0 and line[0] != '#':
						self._add_tile_from_string(line)
	
	def _add_tile_from_string(self, line):
		parts = line.split('\t')
		anim_delay = 4
		if len(parts) == 4 or len(parts) == 5:
			if len(parts) == 5:
				anim_delay = int(parts[4])
			key = trim(parts[0])
			# classification doesn't matter here
			image_files = trim(parts[2])
			if image_files == '':
				image_files = []
			else:
				image_files = image_files.split('|')
			physics = parts[3]
			physics = physics.replace('spikes', 'kill')
			images = []
			tile = TileTemplate(image_files, anim_delay, physics)
			self.tiles[key] = tile
	
	def GetTileTemplate(self, key):
		return self.tiles[key]
	
	def GetTile(self, x, y, key):
		return Tile(x, y, self.GetTileTemplate(key))
	
	# keys are ordered from bottom to top
	def GetCompositeTile(self, x, y, keys):
		templates = []
		for key in keys:
			templates.append(self.GetTileTemplate(key))
		return CompositeTile(x, y, templates)
		
#STATIC
tile_library = TileLibrary()