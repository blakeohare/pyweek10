class Tile:
	def __init__(self, x, y, tile_template):
		self.x = x
		self.y = y
		self.template = tile_template
		self.platforms = None
	
	def get_images(self, counter):
		return [self.template.get_image(counter)]
	
	def get_platforms(self):
		if self.platforms == None:
			self.platforms = self.template.get_platforms(self.x, self.y)
		return self.platforms

class CompositeTile:
	def __init__(self, x, y, tile_templates):
		self.physics_template = self.get_dominant_physics(tile_templates)
		self.templates = tile_templates
		self.platforms = None
		self.x = x
		self.y = y
	
	def get_images(self, counter):
		images = []
		for template in self.templates:
			images.append(template.get_image(counter))
		return images
	
	def get_platforms(self):
		if self.platforms == None:
			self.platforms = self.physics_template.get_platforms(self.x, self.y)
		return self.platforms
	
	def get_dominant_physics(self, tile_templates):
		hierarchy = {
			'passable': 0,
			'water' : 1,
			'platform' : 2,
			'unpassable' : 3
			}
		
		physics = tile_templates[0]
		
		for i in range(1, len(tile_templates)):
			rank_a = hierarchy[physics.physics]
			rank_b = hierarchy[tile_templates[i].physics]
			if rank_b > rank_a:
				physics = tile_templates[i]
		return physics
		
			
	

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