class CreditsScene:
	def __init__(self):
		self.next = self
		self.counter = 0
	
	def Update(self):
		self.counter += 1
	
	def ProcessInput(self, events):
		for event in events:
			pass
	
	def Render(self, screen):
		text = get_text("Credits will go here")
		
		screen.blit(text, (50, 20))
		
	