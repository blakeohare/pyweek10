
class NameEntryScene:
	
	def __init__(self, game, game_slot_index):
		self.next = self
		self.game_slot_index = game_slot_index
		self.counter = 0
		self.cursor_x = 0
		self.cursor_y = 0
		self.mode = 'selection' # 'copy' or 'erase'
		self.text_entry = ''
		self.game = game
		
	def ProcessInput(self, events):
		
		for event in events:
			if event.down:
				if event.key == 'up':
					self.cursor_y = max(0, self.cursor_y - 1)
				elif event.key == 'down':
					self.cursor_y = min(5, self.cursor_y + 1)
				elif event.key == 'left' and self.cursor_y < 5:
					self.cursor_x = max(0, self.cursor_x - 1)
				elif event.key == 'right' and self.cursor_y < 5:
					self.cursor_x = min(7, self.cursor_x + 1)
				elif event.key == 'right' and self.cursor_y == 5 and self.cursor_x < 3:
					self.cursor_x = 3
				elif event.key == 'left' and self.cursor_y == 5 and self.cursor_x >= 3:
					self.cursor_x = 2
				elif event.key in ('start', 'B','Y','A'):
					
					if len(self.text_entry) < 10:
						char = self.current_character()
						name = self.text_entry
						if char == None:
							if self.cursor_x >= 3:
								if len(name) > 0:
									self.game.save_value('name', name)
									self.game.save_value('saved', 1)
									self.game.save_to_file()
									self.next = SelectGameScene(self.game_slot_index)
								else:
									# TODO: play error sound
									pass
							else:
								if self.text_entry == '':
									self.next = SelectGameScene(self.game_slot_index)
								else:
									self.text_entry = self.text_entry[:-1]
						else:	
							self.text_entry += char
				
					
		
	def Render(self, screen):
		
		screen.fill((0,0,0))
		_selectGameBG.Render(screen)
		
		screen.blit(get_text("Name Entry:"), (20, 10))
		
		cursor_coords = self._get_coords(self.cursor_x, self.cursor_y)
		
		name = self.text_entry
		if int(self.counter / 15) % 2 == 1:
			name += '_'
		
		screen.blit(get_text(name), (20, 30))
		
		pygame.draw.circle(screen, (120, 120, 120), (cursor_coords[0] + 4, cursor_coords[1] + 4), 7)
		
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .,-'
		
		for x in range(6):
			for y in range(5):
				index = y * 6 + x
				letter = alphabet[index]
				screen.blit(get_text(letter), self._get_coords(x, y))
		
		numbers = '1234567890'
		
		for x in (0, 1):
			for y in range(5):
				index = y * 2 + x
				number = numbers[index]
				screen.blit(get_text(number), self._get_coords(x + 6, y))
		
		screen.blit(get_text("End"), self._get_coords(3, 5))
		screen.blit(get_text("Back"), self._get_coords(0, 5))
		
	def _get_coords(self, x, y):
		x_left = 20
		y_top = 70
		
		new_x = x_left + x * 18
		new_y = y_top + y * 18
		
		if (x > 5):
			new_x += 10
		
		if y == 5:
			if x >= 3:
				new_x = x_left + 60
			else:
				new_x = x_left
		
		return (new_x, new_y)
	
	def Update(self):
		self.counter += 1
	
	def current_character(self):
		if self.cursor_y == 5:
			return None
		
		if self.cursor_x < 6:
			alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .,-'
			index = self.cursor_x + self.cursor_y * 6
			return alphabet[index]
		
		else:
			x = self.cursor_x - 6
			index = x + self.cursor_y * 2
			numbers = '1234567890'
			return numbers[index]
			
		
		