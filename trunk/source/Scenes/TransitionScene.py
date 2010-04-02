class TransitionScene:
	def __init__(self, from_scene, to_scene, type, duration, params=None):
		self.from_scene = from_scene
		if to_scene != None: to_scene.next = to_scene
		self.to_scene = to_scene
		self.type = type
		self.duration = duration
		self.counter = 0
		self.next = self
		self.temp_screen = pygame.Surface((256, 224))
		self.params = params
		
	def Update(self):
		self.counter += 1
		if self.counter == self.duration:
			self.next = self.to_scene
	
	def ProcessInput(self, events):
		if self.from_scene != None: self.from_scene.ProcessInput(events)
		if self.to_scene != None: self.to_scene.ProcessInput(events)
	
	def Render(self, screen):
		if self.type == 'fadeout':
			if self.counter < self.duration / 2.0:
				opacity = 255 * (1 - 2.0 * self.counter / self.duration)
				opacity = ensure_range(int(opacity), 0, 255)
				self.temp_screen.set_alpha(opacity)
				self.from_scene.Render(self.temp_screen)
			else:
				opacity = 255 * (1 - 2.0 * (self.duration - self.counter) / self.duration)
				opacity = ensure_range(int(opacity), 0, 255)
				self.temp_screen.set_alpha(opacity)
				self.to_scene.Render(self.temp_screen)
			screen.blit(self.temp_screen, (0, 0))
		
		elif self.type == 'fade_and_end':
			self.from_scene.Render(self.temp_screen)
			opacity = 255 * (1 - 2.0 * self.counter / self.duration)
			opacity = ensure_range(int(opacity), 0, 255)
			self.temp_screen.set_alpha(opacity)
			screen.blit(self.temp_screen, (0, 0))
		
		
		elif self.type == 'fade':
			screen.fill((0,0,0))
			self.temp_screen.fill((0,0,0))
			to_opacity = 255 * (self.counter / (self.duration + 0.0))
			to_opacity = ensure_range(int(to_opacity), 0, 255)
			
			self.from_scene.Render(screen)
			self.temp_screen.set_alpha(to_opacity)
			self.to_scene.Render(self.temp_screen)
			screen.blit(self.temp_screen, (0, 0))
		
		elif self.type == 'circle_in':
			radius = int(300 * (1 - self.counter / (0.0 + self.duration)) * 1.5 - 150)
			center_x = self.params[0]
			center_y = self.params[1]
			self.from_scene.Render(screen)
			self.draw_circle(screen, (center_x, center_y), radius)
			
		elif self.type == 'rectangle_down':
			y = 224 * self.counter / self.duration
			self.from_scene.Render(screen)
			pygame.draw.rect(screen, (0,0,0), Rect(0, 0, 256, int(y)))
		
		elif self.type == 'fade_then_circle':
			
			
			if self.counter < self.duration / 2.0:
				#fade
				progress = self.counter / (self.duration / 2.0)
				opacity = int(255 * ensure_range(1 - progress, 0, 1))
				self.from_scene.Render(self.temp_screen)
				self.temp_screen.set_alpha(opacity)
				screen.blit(self.temp_screen, (0,0))
			else:
				#circle
				screen.fill((0,0,0))
				self.to_scene.Render(screen)
				progress = (self.counter / (self.duration + 0.0) - 0.5) * 2
				
				radius = int(progress * 300)
				# promise to only use this transition on PlayScene
				player = self.to_scene.player
				offset = self.to_scene.get_camera_offset()
				#TODO: and camera offset
				center = (int(player.x - offset[0]), int(player.y - offset[1]))
				self.draw_circle(screen, center, radius)
				
				
	def draw_circle(self, surface, center, radius):
		
		center_x = center[0]
		center_y = center[1]
		
		if radius < 1:
			screen.fill((0,0,0))
		else:
			left = center_x - radius
			right = center_x + radius
			top = center_y - radius
			bottom = center_y + radius
			
			#left
			if left > 0:
				pygame.draw.rect(surface, (0, 0, 0), Rect(0, 0, left, 224))
			#right
			if right < 256:
				pygame.draw.rect(surface, (0, 0, 0), Rect(right, 0, 256 - right + 1, 224))
			#top
			if top > 0:
				pygame.draw.rect(surface, (0, 0, 0), Rect(left, 0, right - left, top))
			#bottom
			if bottom < 224:
				pygame.draw.rect(surface, (0, 0, 0), Rect(left, bottom, right - left, 224 - bottom))
			
			count = 10
			for i in range(count):
				a = (0.0 + i) / count
				b = (1.0 + i) / count
				
				xa = math.cos(a * 3.1415926 / 2) * radius
				ya = math.sin(a * 3.1415926 / 2) * radius
				xb = math.cos(b * 3.1415926 / 2) * radius
				yb = math.sin(b * 3.1415926 / 2) * radius
				
				for signs in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
					sx = signs[0]
					sy = signs[1]
					pygame.draw.polygon(surface, (0, 0, 0), [
						(center_x + sx * xa, center_y + sy * ya),
						(center_x + sx * xb, center_y + sy * yb),
						(center_x + sx * xb, sy * radius + center_y),
						(center_x + sx * xa, sy * radius + center_y)])
				
		