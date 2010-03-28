class PlayScreen:
	def __init__(self, level):
		self.counter = 0
		self.render_counter = 0
		
		self.next = self
		self.g = 1.4
		self.level_id = level
		
		wibbly_wobbly = False
		
		self.platforms = {
			'jumpthrough' : [ # left, top, width
				[10, 150, 50],
				[60, 150, 50],
				[50, 102, 50]
				],
			
			'blocking' : [ # left, top, width
				[75, 54, 50]
				],
			
			'solid' : [ #left, top, width, height
				[50, 125, 50, 50]
				],
			
			'inclines' : [
			
				]
		}
		
		self.player = MainCharacter(15, 20)
		
		self.sprites = [self.player]
	
	def get_walls(self, xy):
		return self.platforms['solid']
	
	def get_landing_surfaces_near(self, xy):
		return self.platforms['jumpthrough'] + self.platforms['blocking'] + self.platforms['solid']
	
	def get_ceilings(self, xy):
		platforms = self.platforms['blocking'][:]
		
		for platform in self.platforms['solid']:
			platforms.append([platform[0], platform[1] + platform[3], platform[2]])
		
		return platforms
	
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'B':
				# jump
				if event.down:
					self.player.vy = -15
					self.player.on_ground = False
					self.player.platform = None
				elif self.player.vy < 0:
					self.player.vy = 0
		
		if input.is_key_pressed('left'):
			self.player.left_facing = True
			self.player.vx = -3
		elif input.is_key_pressed('right'):
			self.player.left_facing = False
			self.player.vx = 3
		else:
			self.player.vx = 0
			#TODO: screeching halt
	
	def Update(self):
		self.counter += 1
		
		for sprite in self.sprites:
			
			
			sprite.dx = sprite.vx
			new_x = sprite.x + sprite.dx
			#todo: make sure (new_x, sprite.y) is valid and CROSSABLE
			
			if sprite.dx > 0: #going right
				wall = self.find_leftmost_wall_in_path(sprite.x, new_x, sprite.y)
				if wall != None:
					new_x = wall[0] - 1
			elif sprite.dx < 0: #going left
				wall = self.find_rightmost_wall_in_path(new_x, sprite.x, sprite.y)
				if wall != None:
					new_x = wall[0] + wall[2] + 1
			
			sprite.x = new_x
			
			
			if not sprite.on_ground:
				sprite.vy += self.g
			else:
				sprite.vy = 0
				
			sprite.dy = int(sprite.vy)
			
			new_y = sprite.y + sprite.dy
			
			if sprite.dy > 0:
				# sprite is falling
				
				y_offset = sprite.get_bottom() - sprite.y
				
				highest = self.find_highest_platform_in_path(sprite.x, sprite.y + y_offset, new_y + y_offset)
				
				if highest != None:
					sprite.on_ground = True
					sprite.platform = highest
					self.set_sprite_on_platform(sprite, highest)
				else:
					sprite.y = new_y
			elif sprite.dy < 0:
				
				y_offset = sprite.get_top() - sprite.y + 5 #allow overlap into ceiling of 5 pixels
				
				lowest = self.find_lowest_platform_in_path(sprite.x, new_y + y_offset, sprite.y + y_offset)
				
				if lowest != None:
					sprite.dy = 0
					#TODO: play BONK noise
					sprite.vy = 0
					new_y = lowest[1] + y_offset
					
				else:
					sprite.y = new_y
				#TODO: blocking platforms
				
				
			else:
				if sprite.platform != None:
					platform = sprite.platform
					if sprite.x < platform[0] or sprite.x > platform[0] + platform[2]:
						# player walked off edge of platform
						y = sprite.platform[1]
						new_platform = self.find_highest_platform_in_path(sprite.x, y, y)
						if new_platform != None:
							self.set_sprite_on_platform(sprite, new_platform)
						else:
							sprite.on_ground = False
							sprite.platform = None
				else:
					# This shouldn't happen. But just in case...
					sprite.on_ground = False
	
	def set_sprite_on_platform(self, sprite, platform):
		sprite.y = int(platform[1] - sprite.height + sprite.height / 2) # odd math to keep consistent rounding
	
	def find_leftmost_wall_in_path(self, left_x, right_x, y):
		return self._find_first_wall_in_path(left_x, right_x, y, True)
	
	def find_rightmost_wall_in_path(self, left_x, right_x, y):
		return self._find_first_wall_in_path(left_x, right_x, y, False)
	
	
	def _find_first_wall_in_path(self, left_x, right_x, y, going_right):
		furthest = None
		
		vicinity = ((left_x + right_x) / 2, y)
		platforms = self.get_walls(vicinity)
		
		for platform in platforms:
			if y >= platform[1] and y <= platform[1] + platform[3]:
				wall_x = (platform[0] + platform[2], platform[0])[going_right]
				if left_x <= wall_x and right_x >= wall_x:
					if furthest == None:
						furthest = platform
					elif going_right and furthest[0] > platform[0]:
						furthest = platform
					elif not going_right and furthest[0] + furthest[2] < platform[0] + platform[2]:
						furthest = platform
		return furthest
		
	def _find_first_platform_in_path(self, x, upper_y, lower_y, going_down):
		furthest = None
		
		vicinity = (x, (upper_y + lower_y) / 2) # TODO: remove this and replace with all tile-generated platforms at coordinate X
		if going_down:
			platforms = self.get_landing_surfaces_near(vicinity)
		else:
			platforms = self.get_ceilings(vicinity)
		
		for platform in platforms: 
			if x >= platform[0] and x <= platform[0] + platform[2]:
				if upper_y <= platform[1] and lower_y >= platform[1]:
					if furthest == None:
						furthest = platform
					elif going_down and furthest[1] > platform[1]:
						furthest = platform
					elif not going_down and furthest[1] < platform[1]:
						furthest = platform
		
		return furthest
		
	def find_highest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, True)

	def find_lowest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, False)
		
	def Render(self, screen):
		
		self.render_counter += 1
		
		for platform in self.platforms['jumpthrough']:
			x = platform[0]
			y = platform[1]
			width = platform[2]
			pygame.draw.line(screen, (0, 0, 255), (x, y), (x + width, y))
			
		for platform in self.platforms['blocking']:
			x = platform[0]
			y = platform[1]
			width = platform[2]
			pygame.draw.line(screen, (255, 0, 0), (x, y), (x + width, y))
		
		for platform in self.platforms['solid']:
			x = platform[0]
			y = platform[1]
			width = platform[2]
			height = platform[3]
			pygame.draw.rect(screen, (100, 100, 100), Rect(x, y, width, height))
		
		self.player.draw(screen, self.player.vx != 0, self.counter)
		