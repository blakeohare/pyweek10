	
	

class TileTemplate:
	def __init__(self, image_file_sequence, anim_delay, physics):
		self.img_files = image_file_sequence
		self.images = None
		self.anim_delay = max(anim_delay, 1)
		self.physics = physics
		self.platform_prototypes = {}
		self.types = 'jumpthrough inclines blocking solid'.split(' ')
		
		for type in self.types:
			self.platform_prototypes[type] = []
		
		if self.physics == 'passable':
			pass
		elif self.physics == 'unpassable':
			self.platform_prototypes['solid'].append(Platform('solid', 0, 0, 16, 0, 16, False))
		elif self.physics == 'platform':
			self.platform_prototypes['jumpthrough'].append(Platform('jumpthrough', 0, 0, 16, 0, 0, True))
		elif self.physics == 'solid_platform':
			self.platform_prototypes['blocking'].append(Platform('blocking', 0, 0, 16, 0, 0, False))
		elif self.physics == 'incline_up':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 16, 16, 0, 0, True))
		elif self.physics == 'incline_down':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 0, 16, 16, 0, True))
		elif self.physics == 'shallow_incline_up_lower':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 16, 16, 8, 0, True))
		elif self.physics == 'shallow_incline_up_upper':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 8, 16, 0, 0, True))
		elif self.physics == 'shallow_incline_down_lower':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 8, 16, 16, 0, True))
		elif self.physics == 'shallow_incline_down_upper':
			self.platform_prototypes['incline'].append(Platform('incline', 0, 0, 16, 8, 0, True))
		else:
			# other physics flags will not add platforms but may do other things
			# like affect gravity
			pass
			
		
	def get_platforms(self, pixel_left, pixel_top):
		platforms = {}
		for key in self.types:
			platforms[key] = []
			for platform in self.platform_prototypes[key]:
				platforms[key].append(platform.duplicate(pixel_left, pixel_top))
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