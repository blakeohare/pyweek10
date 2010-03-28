class PlayScreen:
	def __init__(self, level):
		self.counter = 0
		self.render_counter = 0
		
		self.next = self
		self.g = 1
		self.level_id = level
		
		wibbly_wobbly = False
		
		self.platforms = {
			'jumpthrough' : [ # left, top, width
				[10, 150, 50],
				[50, 102, 50]
				],
			
			'blocking' : [
				
				],
			
			'solid' : [
			
				],
			
			'inclines' : [ 
			
				]
		}
		
		self.player = MainCharacter(15, 20)
		
		self.sprites = [self.player]
		
	
	def get_landing_surfaces_near(self, x, y):
		return self.platforms['jumpthrough'] + self.platforms['blocking']
	
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'B':
				# jump
				if event.down:
					self.player.vy = -12
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
				
			sprite.dy = sprite.vy
			
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

	def find_highest_platform_in_path(self, x, upper_y, lower_y):

		highest = None
		
		for platform in self.get_landing_surfaces_near(x, (upper_y + lower_y) / 2): # the mean will do
			if x >= platform[0] and x <= platform[0] + platform[2]:
				if upper_y <= platform[1] and lower_y >= platform[1]:
					if highest == None or highest[1] > platform[1]:
						highest = platform
		
		return highest
					
	
	def Render(self, screen):
		
		self.render_counter += 1
		
		for platform in self.platforms['jumpthrough']:
			x = platform[0]
			y = platform[1]
			width = platform[2]
			pygame.draw.line(screen, (0, 0, 255), (x, y), (x + width, y))
		
		self.player.draw(screen, self.player.vx != 0, self.counter)
		