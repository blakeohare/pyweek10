class ImageLibrary:
	
	def __init__(self):
		self.images = { }
		self.offsets_file = None
		self.offsets = {}
		
	def Get(self, name):
		
		if not (name in self.images.keys()):
			filename = 'images' + os.sep + name.replace('/', os.sep)
			image = pygame.image.load(filename)
			self.images[name] = image
			self.offsets[image] = self._get_offset_from_file(name)
		return self.images[name]
	
	def GetOffset(self, image):
		return self.offsets[image]
	
	def _get_offset_from_file(self, filename):
		if self.offsets_file == None:
			c = open(os.path.join('levels', 'image_metadata', 'offsets.txt'), 'rt')
			lines = trim(c.read()).split('\n')
			c.close()
			
			self.offsets_file = {}
			for line in lines:
				parts = line.split('\t')
				file = parts[0]
				x_offset = int(parts[1])
				y_offset = int(parts[2])
				self.offsets_file[file] = (x_offset, y_offset)
		
		if not filename in self.offsets_file.keys():
			return (0,0)
			
		return self.offsets_file[filename]

#STATIC
images = ImageLibrary()