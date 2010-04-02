class PauseScene:
	def __init__(self, playScene):
		self.next = self
		self.counter = 0
		self.prev = playScene
		self.darken = pygame.Surface((256, 224))
		self.darken.fill((0,0,0))
		self.darken.set_alpha(120)
		self.cursor_y = 0
		self.saved = False
		
	def ProcessInput(self, events):
		for event in events:
			if event.down:
				if event.key == 'start':
					if self.cursor_y == 0:
						self.next = TransitionScene(self, self.prev, 'fade', 10)
						jukebox.MakeLoud()
					elif self.cursor_y == 1:
						games.active_game().save_to_file()
						self.saved = True
					elif self.cursor_y == 2:
						jukebox.Stop()
						jukebox.MakeLoud()
						self.next = TransitionScene(self, TitleScene(), 'fadeout', 30)
				elif event.key == 'left':
					wandStatus.ShiftWand(-1)
				elif event.key == 'right':
					wandStatus.ShiftWand(1)
				elif event.key == 'up':
					self.cursor_y = max(0, self.cursor_y - 1)
				elif event.key == 'down':
					self.cursor_y = min(2, self.cursor_y + 1)
					
	
	def Update(self):
		self.counter += 1
	
	def Render(self, screen):
		self.prev.Render(screen)
		screen.blit(self.darken, (0,0))
		text = get_text("Paused")
		x = 128 - int(text.get_width() / 2)
		y = 20
		screen.blit(text, (x, y))
		
		wands = [
			'basic',
			'ice',
			'fire',
			'lightning',
			'charge'
			]
		
		selected = wandStatus.SelectedWand()
		
		period = 8
		cursor_color = abs(int(self.counter % (period * 2)) - period)
		cursor_color = ensure_range(int(cursor_color * 350.0 / period), 0, 255)
		cursor_color = (cursor_color, cursor_color, cursor_color)
		
		for i in range(5):
			x = 20 + 45 * i
			y = 90
			if selected == i:
				pygame.draw.rect(screen, cursor_color, Rect(x, y, 36, 36))
			if wandStatus.IsKnown(i):
				img = images.Get('wands/magic_' + wands[i] + '.png')
			else:
				img = images.Get('wands/magic_unknown.png')
			screen.blit(img, (x + 2, y + 2))
		
		
		y = 150
		x =  90
		
		text = get_text('Choose Wand Magic:')
		screen.blit(text, (20, 60))
		
		
		i = 0
		for option in ['Resume', ('Save', 'Saved Successfully!')[self.saved], 'Quit']:
			text = get_text(option)
			screen.blit(text, (x, y))
			if self.cursor_y == i:
				screen.blit(images.Get('title_cursor.png'), (x - 15, y + 1))
			y += 18
			i += 1
			
			

class WandStatus:
	def __init__(self):
		self.wand_selected = 0
		self.magic_level = 100

		
	def SelectedWand(self):
		return self.wand_selected
	
	def ShiftWand(self, direction):
		self.SelectWand(self.wand_selected + direction)
	
	def SelectWand(self, wand_index):
	
		self.wand_selected = max(0, min(4, wand_index))
		
	def IsKnown(self, wand_index):
		if wand_index == 0:
			return True
		return games.active_game().get_value('finished_world' + str(wand_index) + '_5') == 1
		
#STATIC
wandStatus = WandStatus()