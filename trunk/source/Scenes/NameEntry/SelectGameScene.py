
class SelectGameScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
		self.cursor_index = 0
		self.mode = 'selection' # 'copy' or 'erase' or paste
		self.text_entry = ''
		self.copy_from = 0
		
		
		
	def ProcessInput(self, events):
		
		enter_pressed = False
		
		for event in events:
			if event.down:
				if event.key == 'up':
					self.cursor_index -= 1
				elif event.key == 'down':
					self.cursor_index += 1
				elif event.key == 'start' or event.key == 'A' or event.key == 'B':
					enter_pressed = True
		if self.cursor_index < 0:
			self.cursor_index = 0
		elif self.cursor_index > 4:
			self.cursor_index = 4
		
		
		if enter_pressed:
			if self.cursor_index == 4:
				if self.mode == 'erase':
					self.mode = 'selection'
				else:
					self.mode = 'erase'
			elif self.cursor_index == 3:
				if self.mode == 'copy' or self.mode == 'paste':
					self.mode = 'selection'
				else:
					self.mode = 'copy'
			else: # 0, 1, 2
				if self.mode == 'selection':
					game = games.get_saved_game(self.cursor_index + 1)
					if game.get_value('saved') == 0:
						self.next = NameEntryScene(game)
					else:
						self.next = None #actual game play! (or probably a brief cut scene depending on the state of the game)
				elif self.mode == 'erase':
					games.erase_game(self.cursor_index + 1)
					self.mode = 'selection'
				elif self.mode == 'copy':
					self.copy_from = self.cursor_index + 1
					self.mode = 'paste'
				elif self.mode == 'paste':
					if self.copy_from == self.cursor_index + 1:
						self.mode = 'copy'
					else:
						self.mode = 'selection'
						games.copy_game(self.copy_from, self.cursor_index + 1)
					
				
	
	def Render(self, screen):
		
		screen.blit(get_text('SELECT GAME'), (10, 10))
		
		x_offset = 10
		
		for slot in (1, 2, 3):
			game = games.get_saved_game(slot)
			is_empty = game.get_value('saved') == 0
			name = game.get_value('name')
			slot_label = get_text('SLOT ' + str(slot) + ': ')
			y = 30 + slot * 16
			mid_y = y + int(slot_label.get_height() / 2)
			
			screen.blit(slot_label, (x_offset, y))
			if is_empty:
				name = get_text('(EMPTY)')
			else:
				name = get_text(name)
			screen.blit(name, (x_offset + slot_label.get_width(), y))
			
			if self.cursor_index + 1 == slot:
				self._draw_cursor_at(x_offset - 5, mid_y)
				
			if self.mode == 'paste' and self.copy_from == slot:
				self._draw_cursor_at(x_offset - 5, mid_y, True)
		
		# copy game
		screen.blit(get_text('COPY GAME'), (x_offset, 120))
		if self.cursor_index == 3:
			self._draw_cursor_at(x_offset - 5, 120 + 4)
		
		# erase game
		screen.blit(get_text('ERASE GAME'), (x_offset, 140))
		if self.cursor_index == 4:
			self._draw_cursor_at(x_offset - 5, 140 + 4)
			
	def _draw_cursor_at(self, x, y, copy_from = False):
		color = (120, 120, 120)
		if copy_from:
			color = (128, 0, 128)
		elif self.mode == 'copy' or self.mode == 'paste':
			color = (0, 0, 255)
		elif self.mode == 'erase':
			color = (255, 0, 0)
		pygame.draw.circle(screen, color, (x, y), 3)
		
		
	def Update(self):
		self.counter += 1
		