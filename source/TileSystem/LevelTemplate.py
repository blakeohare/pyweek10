
class LevelTemplate:
	def __init__(self, tiles, width, values):
		self.width = width
		self.tiles = tiles
		self.values = values
		self.height = int(len(self.tiles) / width)
		self.virtualized_air = tile_library.GetTile(0, 0, '0')
		
		default_values = {
			'victoryX' : 0
		}
		
		for key in default_values.keys():
			if not (key in self.values.keys()):
				self.values[key] = default_values['victoryX']
	
	def get_tile(self, col, row):
		if col < 0 or col >= self.width or row < 0 or row > self.height:
			return self.virtualized_air
		return self.tiles[self.width * row + col]
	
	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height
		