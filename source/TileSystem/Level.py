
class Level:
	def __init__(self, level_template):
		self.level_template = level_template
		self.random_start = 0
	
	def get_tile(self, col, row):
		return self.level_template.get_tile(col, row)
	
	def get_width(self):
		return self.level_template.get_width()
	
	def get_height(self):
		return self.level_template.get_height()
	
	def Refresh(self):
		levels.load_level(self.level_template._remove_me)
		self.level_template = levels.levels[self.level_template._remove_me]
		#levels.load_level(self.level_template._remove_me)
		#levels.levels[self.level_template._remove_me] = self.level_template
	
	def get_enemies(self):
		enemies = []
		for enemy in self.level_template.values['enemies']:
			sprite = None
			x = enemy[1] * 16
			y = enemy[2] * 16
			if enemy[0] == 'bat':
				sprite = EnemyBat(x, y)
			elif enemy[0] == 'skeleton':
				sprite = EnemySkeleton(x, y)
			elif enemy[0] == 'burrower':
				sprite = EnemyBurrow(x, y)
			elif enemy[0] == 'greenblob':
				sprite = EnemyBlob(x, y, 'green')
			elif enemy[0] == 'blueblob':
				sprite = EnemyBlob(x, y, 'blue')
			elif enemy[0] == 'redblob':
				sprite = EnemyBlob(x, y, 'red')
			if sprite != None:
				sprite.x += int(sprite.width / 2)
				sprite.y -= (int(sprite.height / 2) + 1)
				enemies.append(sprite)
		return enemies
				
	
	def get_door_dest(self, x, y):
		for door in self.level_template.values['doors']:
			if door[0] == x and door[1] == y:
				return (door[2], door[3])
		return None
	
	def get_background_image(self, counter):
		if self.level_template.values['storm']:
			foo = int(int(counter % 2000) / 100.0)
			if foo in (1, 3, 11, 15):
				val = int(counter % 100)
				if val >= 2 and val <= 13:
					val = int(val / 2.0)
					return images.Get('backgrounds/stormy' + str(val) + '.png')
		return self.level_template.values['background']
	
	def get_background_offset(self, counter):
		return int(counter * self.level_template.values['background_scroll'])
	
	def get_victory_x(self):
		return self.level_template.values['victoryX']
	
	def get_start_location(self, name=None):
		if name == None:
			name = self.level_template.values['default_start']
		
		if name == None:
			return (1, 1)
		
		return self.level_template.values['start_locations'][name]
	
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
				landing += p['incline']
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
				landing += p['incline']
				y += 1
			x += 1
		
		return landing
	
	