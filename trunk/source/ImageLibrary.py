class ImageLibrary:
	
	def __init__(self):
		self.images = { }
	
	def Get(self, name):
		
		if not (name in self.images.keys()):
			filename = 'images' + os.sep + name.replace('/', os.sep)
			self.images[name] = pygame.image.load(filename)
		return self.images[name]

#STATIC
images = ImageLibrary()