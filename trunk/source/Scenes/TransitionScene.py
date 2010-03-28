class TransitionScene:
	def __init__(self, from_scene, to_scene, type, duration):
		self.from_scene = from_scene
		to_scene.next = to_scene
		self.to_scene = to_scene
		self.type = type
		self.duration = duration
		self.counter = 0
		self.next = self
		self.temp_screen = pygame.Surface((256, 224))
		
	def Update(self):
		self.counter += 1
		if self.counter == self.duration:
			self.next = self.to_scene
	
	def ProcessInput(self, events):
		self.from_scene.ProcessInput(events)
		self.to_scene.ProcessInput(events)
	
	def Render(self, screen):
		if self.type == 'fadeout':
			if self.counter < self.duration / 2.0:
				self.from_scene.Render(self.temp_screen)
				opacity = 255 * (1 - 2.0 * self.counter / self.duration)
			else:
				self.to_scene.Render(self.temp_screen)
				opacity = 255 * (1 - 2.0 * (self.duration - self.counter) / self.duration)
			opacity = ensure_range(int(opacity), 0, 255)
			self.temp_screen.set_alpha(opacity)
			screen.blit(self.temp_screen, (0, 0))
			
		elif self.type == 'fade':
			to_opacity = 255 * (self.counter / self.duration)
			to_opacity = ensure_range(int(to_opacity), 0, 255)
			self.from_scene.Render(screen)
			self.temp_screen.set_alpha(to_opacity)
			self.to_scene.Render(self.temp_screen)
			screen.blit(self.temp_screen, (0, 0))
				
		elif self.type == 'rectangle_down':
			y = 224 * self.counter / self.duration
			self.from_scene.Render(screen)
			pygame.draw.rect(screen, (0,0,0), Rect(0, 0, 256, int(y)))