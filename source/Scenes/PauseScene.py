class PauseScene:
	def __init__(self, playScene):
		self.next = self
		self.counter = 0
		self.prev = playScene
		self.darken = pygame.Surface((256, 224))
		self.darken.fill((0,0,0))
		self.darken.set_alpha(120)
		
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'start' and event.down:
				self.next = TransitionScene(self, self.prev, 'fade', 10)
				jukebox.MakeLoud()
		
	
	def Update(self):
		self.counter += 1
	
	def Render(self, screen):
		self.prev.Render(screen)
		screen.blit(self.darken, (0,0))
		text = get_text("--Ye Olde Pause Screen--")
		x = 128 - int(text.get_width() / 2)
		y = 20
		screen.blit(text, (x, y))