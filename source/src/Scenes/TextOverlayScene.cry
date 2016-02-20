class TextOverlayScene:
	def __init__(self, text, prev, target_scene_afterwards=None):
		self.lines = text.split('\n')
		self.next = self
		self.prev = prev
		self.counter = 0
		self.target_scene_afterwards = target_scene_afterwards
		if target_scene_afterwards == None:
			self.target_scene_afterwards = self.prev
		else:
			self.target_scene_afterwards.from_scene = self
		self.black_box = pygame.Surface((200, 70))
		self.black_box.fill((0,0,0))
		self.quit_counter = -1
		
		self.chunks = [[]]
		while len(self.lines) > 0:
			if len(self.chunks[-1]) < 3:
				self.chunks[-1].append(trim(self.lines[0]))
				self.lines = self.lines[1:]
			else:
				self.chunks.append([])
		
		self.page_counter = 0
		self.page_complete = False
	
	def ProcessInput(self, events):
		for event in events:
			if event.key in ('start', 'A', 'B', 'Y') and event.down:
				if self.page_complete:
					self.chunks = self.chunks[1:]
					self.page_complete = False
					self.page_counter = 0
				else:
					self.page_counter += 1000
					self.page_complete = True
	
	def Update(self):
		self.counter += 1
		self.quit_counter -= 1
		self.page_counter += 1
		
		if self.counter <= 20:
			opacity = int(180 * self.counter / 20.0)
			self.black_box.set_alpha(opacity)
		
		elif self.quit_counter >= 0:
			opacity = int(180 * self.quit_counter / 20.0)
			self.black_box.set_alpha(opacity)
		else:
			self.page_counter += 1
			
		if self.quit_counter == 0:
			self.next = self.target_scene_afterwards
			self.prev.next = self.prev
		elif self.quit_counter < 0 and len(self.chunks) == 0:
			self.quit_counter = 20
			
		
	def Render(self, screen):
		self.prev.Render(screen)
		
		screen.blit(self.black_box, (28, 32))
		
		if len(self.chunks) > 0 and self.page_counter >= 1:
			chunk = self.chunks[0]
			pre_chop = '|'.join(chunk)
			post_chop = pre_chop[:int(self.page_counter / 3.0)]
			self.page_complete = pre_chop == post_chop
			if self.page_complete and int(int(self.counter / 10) % 2) == 0:
				post_chop += '~'
			chunk = post_chop.split('|')
			
			lineA = chunk[0]
			lineB = ''
			lineC = ''
			if len(chunk) > 1:
				lineB = chunk[1]
			if len(chunk) > 2:
				lineC = chunk[2]
			
			lines = (lineA, lineB, lineC)
			y = 40
			x = 35
			for line in lines:
				screen.blit(get_text(line), (x, y))
				y += 18
			