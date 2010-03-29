class Platform:
	def __init__(self, type, left, y_left, width, y_right, height, jumpthrough):
		self.type = type # jumpthrough, blocking, solid, incline
		self.left = left
		self.y_left = y_left
		self.width = width
		self.height = height # only used for solid type
		self.y_right = y_right
		self.jumpthrough = jumpthrough
	
	def get_y_at_x(self, x):
		if self.type == 'incline':
			percentage = (x - self.left + 0.0) / self.width
			return int(self.y_right * percentage + self.y_left * (1 - percentage))
		return self.y_left
	
	def get_x_at_y(self, y):
		# this method is for INCLINES only
		percentage = (y - self.y_left + 0.0) / (self.y_right - self.y_left)
		return int(self.left + percentage * self.width)
	
	def is_x_in_range(self, x):
		return self.left <= x and self.left + self.width >= x
	
	def get_left_wall_x(self):
		return self.left
	
	def get_right_wall_x(self):
		return self.left + self.width
	
	def get_top(self): #assumes non incline type
		return self.y_left 
	
	def get_bottom(self):
		if self.type == 'solid':
			return self.y_left + self.height
		return self.y_left #inclines aren't "bottomed"
	
	def get_closest_terminating_y(self, x):
		if x < self.left:
			return self.y_left
		else:
			return self.y_right
		# this function will not be called when x is in the platform

class PlayScreen:
	def __init__(self, level):
		self.counter = 0
		self.render_counter = 0
		
		self.next = self
		self.g = 1.4
		self.level_id = level
		
		wibbly_wobbly = False
		
		debug_offset = 0
		self.platforms = {
			'jumpthrough' : [ # left, top, width
				Platform('jumpthrough', debug_offset + 0, 150, 40, 150, 0, True),
				Platform('jumpthrough', debug_offset + 40, 150, 40, 150, 0, True),
				Platform('jumpthrough', debug_offset + 120, 110, 40, 110, 0, True),
				Platform('jumpthrough', debug_offset + 200, 150, 40, 150, 0, True)
				],
			
			'blocking' : [ # left, top, width
				Platform('blocking', debug_offset + 140, 40, 80, 40, 0, False)
				],
			
			'solid' : [ #left, top, width, height
				Platform('solid', debug_offset + 220, 20, 30, 20, 50, False)
				],
			
			'inclines' : [ #left, left_top, width, right_top
				Platform('incline', debug_offset + 80, 150, 40, 110, 0, True),
				Platform('incline', debug_offset + 160, 110, 40, 150, 0, True)
				]
		}
		
		self.player = MainCharacter(15, 20)
		
		self.sprites = [self.player]
	
	def get_walls(self, xy):
		return self.platforms['solid']
	
	def get_landing_surfaces_near(self, xy):
		platforms = self.platforms['jumpthrough'] + self.platforms['blocking'] + self.platforms['solid']
		x = xy[0]
		for incline in self.platforms['inclines']:
			if incline.is_x_in_range(x):
				platforms.append(incline)
		return platforms
	
	def get_ceilings(self, xy):
		return self.platforms['blocking'] + self.platforms['solid']
	
	def get_just_inclines(self):
		return self.platforms['inclines']
	
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'B':
				# jump
				if event.down and self.player.on_ground:
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
			
			if sprite.dx > 0: #going right
				wall = self.find_leftmost_wall_in_path(sprite.x, new_x, sprite.y)
				if wall != None:
					new_x = wall.get_left_wall_x() - 1
			elif sprite.dx < 0: #going left
				wall = self.find_rightmost_wall_in_path(new_x, sprite.x, sprite.y)
				if wall != None:
					new_x = wall.get_right_wall_x() + 1
			
			# player may have possibly jumped through an incline
			if new_x != sprite.x and sprite.platform == None:
				
				inclines = []
				
				for incline in self.get_just_inclines():
					
					#we're only interested in inclines in the horizontal component
					top = min(incline.y_left, incline.y_right)
					bottom = max(incline.y_left, incline.y_right)
					if sprite.y >= top and sprite.y <= bottom:
						if new_x > sprite.x and incline.y_left > incline.y_right:
							inclines.append(incline)
						elif new_x < sprite.x and incline.y_left < incline.y_right:
							inclines.append(incline)
				
				for incline in inclines:
					starts_above = sprite.y < incline.get_y_at_x(sprite.x)
					ends_above = sprite.y < incline.get_y_at_x(new_x)
					
					if starts_above and not ends_above:
						new_x = incline.get_x_at_y(sprite.y)
						sprite.platform = incline
						sprite.on_ground = True
						sprite.vy = 0
						break
			
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
					new_y = lowest.get_bottom() + y_offset
					
				else:
					sprite.y = new_y
				
			else:
				if sprite.platform != None:
					platform = sprite.platform
					if platform.is_x_in_range(sprite.x):
						self.set_sprite_on_platform(sprite, platform)
					else:
						# player walked off edge of platform
						
						new_platform_found = False
						
						# which way?
						if sprite.x < platform.left:
							# walked off left
							for left_platform in self.get_landing_surfaces_near((platform.left - 1, sprite.y)):
								
								# check to see if the right side of this platform is vertically aligned with 
								# the left side of the one you walked off
								if abs(left_platform.left + left_platform.width - platform.left) <= 1:
									
									# check to see if they're vertically aligned
									if abs(left_platform.y_right - platform.y_left) <= 1:
										sprite.platform = left_platform
										break
								
						else:
							# walked off right
							for right_platform in self.get_landing_surfaces_near((platform.left + platform.width + 1, sprite.y)):
								
								# check to see if the left side of this platform is vertically aligned with 
								# the right side of the one you walked off
								if abs(right_platform.left - (platform.left + platform.width)) <= 1:
									
									# check to see if they're vertically aligned
									if abs(right_platform.y_left - platform.y_right) <= 1:
										sprite.platform = right_platform
										break
						
						# if no new platform was found...
						if sprite.platform == platform:
							#the sprite has fallen off the edge
							sprite.on_ground = False
							sprite.platform = None
							
				else:
					# This shouldn't happen. But just in case...
					sprite.on_ground = False
	
	def set_sprite_on_platform(self, sprite, platform):
		sprite.y = int(platform.get_y_at_x(sprite.x) - sprite.height + sprite.height / 2) # odd math to keep consistent rounding
	
	def find_leftmost_wall_in_path(self, left_x, right_x, y):
		return self._find_first_wall_in_path(left_x, right_x, y, True)
	
	def find_rightmost_wall_in_path(self, left_x, right_x, y):
		return self._find_first_wall_in_path(left_x, right_x, y, False)
	
	
	def _find_first_wall_in_path(self, left_x, right_x, y, going_right):
		furthest = None
		
		vicinity = ((left_x + right_x) / 2, y)
		platforms = self.get_walls(vicinity)
		
		for platform in platforms: # all platforms are guaranteed to be solid type
			if y >= platform.get_top() and y <= platform.get_bottom():
				if going_right:
					wall_x = platform.left
				else:
					wall_x = platform.left + platform.width
					
				if left_x <= wall_x and right_x >= wall_x:
					if furthest == None:
						furthest = platform
					elif going_right and furthest.left > platform.left:
						furthest = platform
					elif not going_right and furthest.left + furthest.width < platform.left + platform.width:
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
			if platform.is_x_in_range(x):
				platform_y = platform.get_y_at_x(x)
				if upper_y <= platform_y and lower_y >= platform_y:
					if furthest == None:
						furthest = platform
					elif going_down and furthest.get_y_at_x(x) > platform_y:
						furthest = platform
					elif not going_down and furthest.get_bottom() < platform.get_bottom():
						furthest = platform
		
		return furthest
		
	def find_highest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, True)

	def find_lowest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, False)
		
	def Render(self, screen):
		
		self.render_counter += 1
		
		for platform in self.platforms['jumpthrough']:
			x = platform.left
			y = platform.y_left
			width = platform.width
			pygame.draw.line(screen, (0, 0, 255), (x, y), (x + width, y))
			
		for platform in self.platforms['blocking']:
			x = platform.left
			y = platform.y_left
			width = platform.width
			pygame.draw.line(screen, (255, 0, 0), (x, y), (x + width, y))
		
		for platform in self.platforms['solid']:
			x = platform.left
			y = platform.y_left
			width = platform.width
			height = platform.height
			pygame.draw.rect(screen, (100, 100, 100), Rect(x, y, width, height))
		
		for platform in self.platforms['inclines']:
			x = platform.left
			y_left = platform.y_left
			width = platform.width
			y_right = platform.y_right
			pygame.draw.line(screen, (0, 0, 255), (x, y_left), (x + width, y_right))
		
		self.player.draw(screen, self.player.vx != 0, self.counter)
		