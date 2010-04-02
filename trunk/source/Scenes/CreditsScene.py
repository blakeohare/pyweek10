class CreditsScene:
	def __init__(self):
		self.next = self
		self.counter = 0
		self.pages = """0
Programmed By:
Blake O'Hare
---0
Pixel Art:
Spears Dracona
---0
CutScene Art:
Mr. Falun
---0
Music:
Devin McGinty
Mr. I Kan Reed
---0
Level Design:
Brett S.
Blake O'Hare
---0
Assistant Programming:
Mr. Falun
---0
Story:
Mr. Falun
Brett S.
Blake O'Hare
---50
Special Thanks to:
#pygame on irc.freenode.com
www.pyweek.org
Pappy Frank's Pizza
l'Hopital's Rule
Kitty Litter
Whigs
The Floating Point Arithmetic Fairy
Crumpets
The letter Y
---0
...and you for actually 
playing this far!
---0
Lines of Python code:
3947""".split('---')
		self.page_counter = 0
		self.temp_screen = pygame.Surface((256, 224))
	
	def Update(self):
		self.counter += 1
		opacity = 0
		
		if self.counter > 30:
			self.page_counter += 1
			page_duration = 90
			
			opacity = 255
			if len(self.pages) > 0:
				page = self.pages[0]
				page_duration += int(page.split('\n')[0])
				#print self.page_counter
				if self.page_counter < 30:
					opacity = int(255 * self.page_counter / 30.0 )
				elif self.page_counter > 30 + page_duration:
					opacity = 255 - int(255 * (self.page_counter - 30 - page_duration) / 30.0)
					
			if self.page_counter >= 30 + 30 + page_duration:
				opacity = 0
				self.pages = self.pages[1:]
				self.page_counter = 0
			
		self.temp_screen.set_alpha(opacity)
		
	def ProcessInput(self, events):
		for event in events:
			pass
	
	def Render(self, screen):
		
		screen.fill((0,0,0))
		self.temp_screen.fill((0,0,0))
		if len(self.pages) > 0 and self.page_counter > 0:
			lines = trim(self.pages[0]).split('\n')[1:]
			height = len(lines) * 18
			y = int((224 - height) / 2.0)
			for line in lines:
				text = get_text(trim(line))
				x = int((256 - text.get_width()) / 2.0)
				self.temp_screen.blit(text, (x, y))
				y += 18
		screen.blit(self.temp_screen, (0, 0))
		
	