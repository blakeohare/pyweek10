class TitleScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
		
	
	def Render(self, screen):
		screen.blit(images.Get('title.png'), (0, 0))
	
	def Update(self):
		self.counter += 1