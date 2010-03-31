class WibblyWobblyRenderer:
	
	def __init__(self):
		
		self.sliver_width = 4
		sliver_count = int(256 / self.sliver_width + 1)
		self.slivers = []
		
		for i in range(sliver_count):
			self.slivers.append(pygame.Surface((self.sliver_width, 224)))
		
		self.color_fade_surface = pygame.Surface((256, 224))
		
	def get_max_severity(self):
		return 300
	
	def render_color_fade(self, screen, counter, severity):
		redness = ensure_range(int(255 * abs((counter % 30) - 15.0) / 15.0), 0, 255)
		blueness = 255 - redness
		opacity = int(255 * 0.8 * min(self.get_max_severity(), severity) / (self.get_max_severity() + 0.0))
		self.color_fade_surface.fill((redness, 0, blueness))
		self.color_fade_surface.set_alpha(opacity)
		screen.blit(self.color_fade_surface, (0, 0))
	
	def render(self, screen, counter, severity):
		
		severity = min(self.get_max_severity(), severity)
		percentage = int(10 * (0.0 + severity) / self.get_max_severity()) / 10.0
		
		x_offset = 0
		for sliver in self.slivers:
			sliver.blit(screen, (-x_offset, 0))
			x_offset += self.sliver_width
		
		
		screen.fill((0, 0, 0))
		
		x_offset = 0
		i = 0
		for sliver in self.slivers:
			y = int(math.sin((i + counter / 2) * 3.14159265 * 2 / 24) * 9 * percentage)
			screen.blit(sliver, (x_offset, y))
			x_offset += self.sliver_width
			i += 1
		
			