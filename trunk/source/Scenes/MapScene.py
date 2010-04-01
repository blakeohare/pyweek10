class MapScene:
	def __init__(self, world_num, level, level_to=None):
		games.active_game().save_value('intro_shown', 1)
		self.counter = 0
		self.next = self
		self.world_num = world_num
		self.location = level
		self.nodes = self._read_map_file()
		#TODO: set initial location from save game
		self.bg_image = None
		if level_to != None:
			self.destination = level_to
		else:
			self.destination = self.location
		self.move_counter = 0
		self.facing_left = False
		
	def Update(self):
		self.counter += 1
		
		if self.counter == 1:
			jukebox.PlayMapMusic()
		
		if self.destination != self.location:
			self.move_counter += 1
			
			if self.move_counter >= 15:
				self.move_counter = 0
				self.location = self.destination
				
				screenchange = None
				if self.location == 'prev':
					screenchange = MapScene(self.world_num - 1, 'next', '5')
				elif self.location == 'next':
					screenchange = MapScene(self.world_num + 1, 'prev', '1')
				if screenchange != None:
					self.next = TransitionScene(self, screenchange, 'fadeout', 30)
		
	
	def Render(self, screen):
		
		if self.bg_image == None:
			self.bg_image = self.generate_map()
		
		screen.blit(self.bg_image, (0, 0))
		
		walking = self.location != self.destination
		direction = ('right','left')[self.facing_left]
		img = 'sprites/ClumsyWizard/' + direction
		if walking:
			img += 'walk' + str(int(int(self.counter / 3) % 3)) + '.png'
		else:
			img += 'stand.png'
		
		character = images.Get(img)
		start_node = self.nodes[self.location]
		end_node = self.nodes[self.destination]
		start_x = start_node['x']
		start_y = start_node['y']
		end_x = end_node['x']
		end_y = end_node['y']
		x = int(start_x * (15 - self.move_counter) / 15.0 + end_x * self.move_counter / 15.0 - character.get_width() / 2)
		y = int(start_y * (15 - self.move_counter) / 15.0 + end_y * self.move_counter / 15.0 - character.get_height() / 2)
		screen.blit(character, (x, y - 10))
	
	def ProcessInput(self, events):
		for event in events:
			if self.move_counter == 0:
				node = self.nodes[self.location]
				if event.down and event.key in ('left','right','down','up'):
					for connection in node['connections']:
						if connection[1] == event.key:
							if node['completed'] or self.nodes[connection[0]]['completed']:
								self.destination = connection[0]
								self.facing_left = self.nodes[self.location]['x'] > self.nodes[self.destination]['x']
							break
				elif event.down and event.key in ('start', 'B', 'A'):
					nextScene = PlaySceneInfoScene(self.world_num, self.location)
					self.next = TransitionScene(self, nextScene, 'fadeout', 30)
					jukebox.FadeOut(2)
		
	
	def generate_map(self):
		original = images.Get('maps/world_' + str(self.world_num) + '.png')
		background = pygame.Surface((256, 224))
		background.blit(original, (0, 0))
		
		nodes = self.nodes
		
		color = (255, 255, 255)
		complete_color = (0, 128, 0)
		incomplete_color = (255, 0, 0)
		for start in nodes.keys():
			start_x = nodes[start]['x']
			start_y = nodes[start]['y']
			
			for end in nodes[start]['connections']:
				end_x = nodes[end[0]]['x']
				end_y = nodes[end[0]]['y']
				
				for i in range(50):
					x = int(start_x * i / 50.0 + end_x * (50 - i) / 50.0)
					y = int(start_y * i / 50.0 + end_y * (50 - i) / 50.0)
					pygame.draw.circle(background, color, (x, y), 5)
		for node in nodes.values():
			color = incomplete_color
			if node['completed'] == 1:
				color = complete_color
			pygame.draw.circle(background, (0, 0, 0), (node['x'], node['y']), 9)
			pygame.draw.circle(background, color, (node['x'], node['y']), 7)
			
		return background
	
	def _read_map_file(self):
		c = open(os.path.join('levels', 'world_map', 'world_' + str(self.world_num) + '.txt'), 'rt')
		lines = trim(c.read()).split('\n')
		c.close()
		nodes = {}
		connections = False
		for line in lines:
			line = trim(line)
			if not connections:
				if line == '#connections':
					connections = True
				else:
					parts = line.split('\t')
					id = parts[0]
					if self.location == '': #TODO: remove this when start location is loaded from saved game
						self.location = id
					coords = parts[1].split(',')
					x = int(coords[0])
					y = int(coords[1])
					nodes[id] = {
						'id' : id,
						'x' : x,
						'y' : y,
						'connections' : [],
						'completed' : (games.active_game().get_value('finished_world' + str(self.world_num) + '_' + id) == 1)
					}
			else:
				parts = line.split('\t')
				left = parts[0]
				right = parts[1]
				direction = parts[2]
				nodes[left]['connections'].append((right, direction))
				nodes[right]['connections'].append((left, self._swap_direction(direction)))
				
		return nodes
	
	def _swap_direction(self, d):
		if d == 'right': return 'left'
		if d == 'left' : return 'right'
		if d == 'down' : return 'up'
		if d == 'up'   : return 'down'