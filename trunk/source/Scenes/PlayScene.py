class Platform:
	def __init__(self, type, left, y_left, width, y_right, height, jumpthrough):
		self.type = type # jumpthrough, blocking, solid, incline
		self.left = left
		self.y_left = y_left
		self.width = width
		self.height = height # only used for solid type
		self.y_right = y_right
		self.jumpthrough = jumpthrough
	
	def duplicate(self, x_offset, y_offset):
		return Platform(type,
			self.left + x_offset,
			self.y_left + y_offset,
			self.width,
			self.y_right + y_offset,
			self.height,
			self.jumpthrough)
	
	def get_y_at_x(self, x):
		if self.type == 'incline':
			percentage = (x - self.left + 0.0) / self.width
			return int(self.y_right * percentage + self.y_left * (1 - percentage))
		return self.y_left
	
	def get_x_at_y(self, y):
		# this method is for INCLINES only
		# y MUST be in the range of this incline
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
		
		level = level + 'a' #TODO: remove this
		self.level_id = level
		
		self.level_info = levels.get_level(self.level_id)
		
		wibbly_wobbly = False
		
		debug_offset = 0
		self.platforms = {
			'jumpthrough' : [ # left, top, width
				#Platform('jumpthrough', debug_offset + 0, 150, 40, 150, 0, True),
				#Platform('jumpthrough', debug_offset + 40, 150, 40, 150, 0, True),
				#Platform('jumpthrough', debug_offset + 120, 110, 40, 110, 0, True),
				#Platform('jumpthrough', debug_offset + 200, 150, 20, 150, 0, True)
				],
			
			'blocking' : [ # left, top, width
				#Platform('blocking', debug_offset + 40, 60, 80, 60, 0, False),
				#Platform('blocking', debug_offset + 4, 100, 30, 100, 0, False)
				],
			
			'solid' : [ #left, top, width, height
				#Platform('solid', debug_offset + 120, 40, 30, 40, 20, False),
				#Platform('solid', debug_offset + 241, 100, 60, 100, 100, False)
				],
			
			'inclines' : [ #left, left_top, width, right_top
				#Platform('incline', debug_offset + 80, 150, 40, 110, 0, True),
				#Platform('incline', debug_offset + 160, 110, 40, 150, 0, True),
				#Platform('incline', debug_offset + 220, 150, 20, 140, 0, True)
				
				]
		}
		
		self.player = MainCharacter(15, 20)
		
		self.sprites = [self.player]
	
	def get_walls(self, x_left, x_right, y_top, y_bottom):
		tile_left = (x_left - 1) >> 4
		tile_right = (x_right + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		platforms = []
		
		for tile_x in range(tile_left, tile_right + 1):
			for tile_y in range(tile_top, tile_bottom + 1):
				platforms += self.level_info.get_tile(tile_x, tile_y).get_platforms()['solid']
				
		return platforms
	
	def get_landing_surfaces(self, x, y_top, y_bottom):
		tile_left = (x - 1) >> 4
		tile_right = (x + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		return self.level_info.get_landing_platforms_in_rectangle(tile_left - 1, tile_right + 1, tile_top, tile_bottom)
	
	def get_ceilings(self, x, y_top, y_bottom):
	
		tile_left = (x - 1) >> 4
		tile_right = (x + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		return self.level_info.get_ceilings_in_rectangle(tile_left, tile_right, tile_top, tile_bottom)
	
	def get_just_inclines(self, x_left, x_right, y_top, y_bottom):
	
		tile_left = (x_left - 1) >> 4
		tile_right = (x_right + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		return self.level_info.get_inclines_in_rectangle(tile_left, tile_right, tile_top, tile_bottom)
	
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
			new_x = int(sprite.x + sprite.dx)
			
			if sprite.dx > 0: #going right
				wall = self.find_leftmost_wall_in_path(sprite.x, new_x, sprite.get_head_bonk_top(), sprite.get_bottom())
				if wall != None:
					new_x = wall.get_left_wall_x() - 1
			elif sprite.dx < 0: #going left
				wall = self.find_rightmost_wall_in_path(new_x, sprite.x, sprite.get_head_bonk_top(), sprite.get_bottom())
				if wall != None:
					new_x = wall.get_right_wall_x() + 1
			
			# player may have possibly jumped through an incline
			if new_x != sprite.x and not sprite.on_ground:
				
				inclines = []
				
				sprite_bottom = sprite.get_bottom()
				
				for incline in self.get_just_inclines(min(new_x, sprite.x) - 2, max(new_x, sprite.x) + 2, sprite.y - 1, sprite.y + 1):
					
					#we're only interested in inclines in the horizontal component
					top = min(incline.y_left, incline.y_right)
					bottom = max(incline.y_left, incline.y_right)
					if sprite_bottom >= top and sprite_bottom <= bottom:
						#if new_x > sprite.x and incline.y_left > incline.y_right:
							inclines.append(incline)
						#elif new_x < sprite.x and incline.y_left < incline.y_right:
						#	inclines.append(incline)
				
				for incline in inclines:
				
					starts_above = sprite_bottom < incline.get_y_at_x(sprite.x)
					ends_above = sprite_bottom < incline.get_y_at_x(new_x)
					
					if starts_above and not ends_above:
						sprite.x = incline.get_x_at_y(sprite.y)
						
						#if incline.is_x_in_range(new_x):
						sprite.platform = incline
						sprite.on_ground = True
						sprite.vy = 0
						self.set_sprite_on_platform(sprite, incline)
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
			elif sprite.dy <= 0 and sprite.platform == None:
				
				y_offset = sprite.get_head_bonk_top() - sprite.y
				
				lowest = self.find_lowest_platform_in_path(sprite.x, new_y + y_offset, sprite.y + y_offset)
				
				if lowest != None:
					sprite.dy = 0
					sprite.vy = 0
					new_y = lowest.get_bottom() + y_offset
					#TODO: play BONK noise
					
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
							left = platform.left
							for left_platform in self.get_landing_surfaces(left - 1, sprite.y - 18, sprite.y + 18):
								
								# check to see if the right side of this platform is vertically aligned with 
								# the left side of the one you walked off
								if abs(left_platform.left + left_platform.width - platform.left) <= 1:
									
									# check to see if they're vertically aligned
									if abs(left_platform.y_right - platform.y_left) <= 1:
										sprite.platform = left_platform
										break
								
						else:
							# walked off right
							right = platform.left + platform.width
							for right_platform in self.get_landing_surfaces(right + 1, sprite.y - 18, sprite.y + 18):
								
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
	
	def set_sprite_on_platform(self, sprite, platform):
		sprite.y = int(platform.get_y_at_x(sprite.x) - sprite.height + sprite.height / 2) # odd math to keep consistent rounding
	
	def find_leftmost_wall_in_path(self, left_x, right_x, y_top, y_bottom):
		return self._find_first_wall_in_path(left_x, right_x, y_top, y_bottom, True)
	
	def find_rightmost_wall_in_path(self, left_x, right_x, y_top, y_bottom):
		return self._find_first_wall_in_path(left_x, right_x, y_top, y_bottom, False)
	
	
	def _find_first_wall_in_path(self, left_x, right_x, y_top, y_bottom, going_right):
		furthest = None
		
		platforms = self.get_walls(left_x, right_x, y_top, y_bottom)
		
		for platform in platforms: # all platforms are guaranteed to be solid type
			if not (y_bottom <= platform.get_top() or y_top > platform.get_bottom()):
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
		
		if going_down:
			platforms = self.get_landing_surfaces(x, upper_y, lower_y)
		else:
			platforms = self.get_ceilings(x, upper_y, lower_y)
		
		for platform in platforms: 
			if platform.is_x_in_range(x):
				if going_down:
					platform_y = platform.get_y_at_x(x)
				else:
					platform_y = platform.get_bottom()
					
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
		
		for row in range(self.level_info.get_height()):
			for col in range(self.level_info.get_width()):
				x = col * 16
				y = row * 16
				tile = self.level_info.get_tile(col, row)
				imgs = tile.get_images(self.render_counter)
				if imgs != None:
					for img in imgs:
						if img != None:
							screen.blit(img, (x, y))
				
		
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
		