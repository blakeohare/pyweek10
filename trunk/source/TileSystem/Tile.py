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
		
		