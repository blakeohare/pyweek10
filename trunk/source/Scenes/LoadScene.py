class LoadScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
	
	def ProcessInput(self, events):
		pass
		
	def Render(self, screen):
		screen.blit(images.Get('load_splash.png'), (0, 0))
	
	def Update(self):
		self.counter += 1
		
		if self.counter > 2: #don't check this in
			self.next = TitleScene()