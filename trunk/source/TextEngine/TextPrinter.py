class TextPrinter:
	
	def __init__(self):
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		self.space_width = 8
		
		self.images = {
			' ' : pygame.Surface((self.space_width, 1))
			}
		self.text_cache = {}
		
		for char in alphabet:
			self.images[char] = images.Get('text/lower/' + char + '.png')
		
		alphabet = alphabet.upper()
		
		for char in alphabet:
			self.images[char] = images.Get('text/upper/' + char + '.png')
		
		nums = '0123456789'
		
		for char in nums:
			self.images[char] = images.Get('text/number/' + char + '.png')
		
		punctuation = [
			('apostrophe', "'"),
			('asterisk', '*'),
			('close_paren', ')'),
			('colon', ':'),
			('comma', ','),
			('exclaim', '!'),
			('hyphen', '-'),
			('open_paren', '('),
			('open_quote', '"'),
			#TODO: close quote
			('period', '.'),
			('ques', '?')]
		
		for char_key in punctuation:
			file = char_key[0]
			char = char_key[1]
			self.images[char] = images.Get('text/number/' + file + '.png')
			
	def get_rendered_text(self, string):
		
		if string == None or len(string) == 0:
			string = ' '
		
		if string in self.text_cache.keys():
			return self.text_cache[string]
		
		surface = pygame.Surface(self.calc_size(string))
		x = 0
		for char in string:
			img = self.get_image_for_char(char)
			surface.blit(img, (x, 0))
			x += img.get_width()
		
		self.text_cache[string] = surface
		return surface
		
	
	def calc_size(self, string):
		height = 8
		width = 0
		max_height = 0
		
		for char in string:
			img = self.get_image_for_char(char)
			width += img.get_width()
			height = max(max_height, img.get_height())
		return (width, height)
	
	def get_image_for_char(self, char):
		if not (char in self.images.keys()):
			char = '?'
		return self.images[char]
		