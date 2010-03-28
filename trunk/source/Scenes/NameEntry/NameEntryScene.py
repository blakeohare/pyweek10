
class NameEntryScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
		self.cursor_x = 0
		self.cursor_y = 0
		self.mode = 'selection' # 'copy' or 'erase'
		self.text_entry = ''
		
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
				elif event.key == 'start' or event.key == 'A':
					
					if len(self.text_entry) < 10:
						self.text_entry
					
				elif event.key == 'B':
					backspaced = True
		
					
		
	def Render(self, screen):
		
		cursor_coords = self._get_coords(self.cursor_x, self.cursor_y)
		
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
		
		screen.blit(get_text("END"), self._get_coords(0, 5))
		
	def _get_coords(self, x, y):
		x_left = 20
		y_top = 50
		
		new_x = x_left + x * 15
		new_y = y_top + y * 15
		
		if (x > 5):
			new_x += 10
		
		if y == 5:
			new_x = x_left + 50
		
		return (new_x, new_y)
	
	def Update(self):
		self.counter += 1
	
	def CurrentCharacter(self):
		if self.cursor_y == 5:
			return None
		
		#if 
		