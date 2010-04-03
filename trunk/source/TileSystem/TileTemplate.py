	
	

class TileTemplate:
	def __init__(self, image_file_sequence, anim_delay, physics):
		self.img_files = image_file_sequence
		self.images = None
		self.anim_delay = max(anim_delay, 1)
		self.physics = physics
		self.platform_prototypes = {}
		self.is_victory = False
		
		self.water_modifier = False
		self.ladder_modifier = False
		self.kill_modifier = False
		self.ouch_modifier = False
	
		self.has_up_inclines = False
		self.has_down_inclines = False
		
		
		self.types = 'jumpthrough ignored_solid incline blocking solid'.split(' ')
		
		
		
		for physics in self.physics.split('|'):
			
			for type in self.types:
				self.platform_prototypes[type] = []
			
			if physics == 'passable' or self.physics == '':
				pass
			elif physics == 'unpassable':
				self.platform_prototypes['solid'].append(Platform('solid', 0, 0, 16, 0, 16, False))
				self.platform_prototypes['blocking'].append(Platform('blocking', 0, 0, 16, 0, 0, False))
				self.platform_prototypes['blocking'].append(Platform('blocking', 0, 16, 16, 16, 0, False))
			elif physics == 'platform':
				self.platform_prototypes['jumpthrough'].append(Platform('jumpthrough', 0, 0, 16, 0, 0, True))
			elif physics == 'solid_platform':
				self.platform_prototypes['blocking'].append(Platform('blocking', 0, 0, 16, 0, 0, False))
			elif physics == 'incline_up':
				self.has_up_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 16, 16, 0, 0, True))
			elif physics == 'incline_down':
				self.has_down_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 0, 16, 16, 0, True))
			elif physics == 'shallow_incline_up_lower':
				self.has_up_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 16, 16, 8, 0, True))
			elif physics == 'shallow_incline_up_upper':
				self.has_up_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 8, 16, 0, 0, True))
			elif physics == 'shallow_incline_down_lower':
				self.has_down_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 8, 16, 16, 0, True))
			elif physics == 'shallow_incline_down_upper':
				self.has_down_inclines = True
				self.platform_prototypes['incline'].append(Platform('incline', 0, 0, 16, 8, 0, True))
			elif physics == 'water':
				self.water_modifier = True
			elif physics == 'ladder':
				self.ladder_modifier = True
			elif physics == 'kill':
				self.kill_modifier = True
			elif physics == 'ouch':
				self.ouch_modifier = True
			else:
				# other physics flags will not add platforms but may do other things
				# like affect gravity
				print ("UNKNOWN PHYSICS: ", self.physics)
				pass
			
	def is_victory(self):
		return self.is_victory
	
	def get_platforms(self, pixel_left, pixel_top, ignore_left_walls, ignore_right_walls):
		platforms = {}
		
		for key in self.types:
			platforms[key] = []
			
			for platform in self.platform_prototypes[key]:
				new_platform = None
				if key == 'solid':
					if ignore_left_walls and ignore_right_walls:
						continue
					elif ignore_left_walls:
						new_platform = platform.duplicate_right(pixel_left, pixel_top)
					elif ignore_right_walls:
						new_platform = platform.duplicate_left(pixel_left, pixel_top)
				
				if new_platform == None:
					new_platform = platform.duplicate(pixel_left, pixel_top)
				
				platforms[key].append(new_platform)
		return platforms
		
		
	def get_image(self, counter):
		if self.images == None:
			self.images = []
			for file in self.img_files:
				path = 'tiles/' + file + '.png'
				self.images.append(images.Get(path))
		
		if len(self.images) == 0:
			return None
		
		
		return self.images[int(int(counter / self.anim_delay) % len(self.images))]