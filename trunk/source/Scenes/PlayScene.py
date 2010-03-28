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
				[50, 102, 50]
				],
			
			'blocking' : [
				[75, 54, 50]
				],
			
			'solid' : [
			
				],
			
			'inclines' : [
			
				]
		}
		
		self.player = MainCharacter(15, 20)
		
		self.sprites = [self.player]
		
	
	def get_landing_surfaces_near(self, xy):
		return self.platforms['jumpthrough'] + self.platforms['blocking']
	
	def get_ceilings(self, xy):
		return self.platforms['blocking']
	
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

	def _find_first_platform_in_path(self, x, upper_y, lower_y, going_down):
		highest = None
		
		vicinity = (x, (upper_y + lower_y) / 2) # TODO: remove this and replace with all tile-generated platforms at coordinate X
		if going_down:
			platforms = self.get_landing_surfaces_near(vicinity)
		else:
			platforms = self.get_ceilings(vicinity)
		
		for platform in platforms: 
			if x >= platform[0] and x <= platform[0] + platform[2]:
				if upper_y <= platform[1] and lower_y >= platform[1]:
					if highest == None:
						highest = platform
					elif going_down and highest[1] > platform[1]:
						highest = platform
					elif not going_down and highest[1] < platform[1]:
						highest = platform
		
		return highest
		
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
		
		self.player.draw(screen, self.player.vx != 0, self.counter)
		