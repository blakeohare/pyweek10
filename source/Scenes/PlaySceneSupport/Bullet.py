class Bullet:
	def __init__(self, going_left, x, y, magic):
		self.x = x
		self.y = y
		self.going_left = going_left
		self.x += (8,-8)[going_left]
		self.magic = magic # selected wand index at the moment of firing
		self.name = ['basic','ice','fire','lightning','charge'][magic]
		self.expired = False
		self.lifetime = 0
		
	def draw(self, screen, camera_x, camera_y):
		file = 'wands/shoot_' + self.name + str(int((self.lifetime / 2) % 3)) + '.png'
		img = images.Get(file)
		x = self.x - camera_x - int(img.get_width() / 2)
		y = self.y - camera_y - int(img.get_height() / 2)
		screen.blit(img, (x, y))
		
	def update(self):
		self.lifetime += 1
		if self.going_left:
			self.x -= 8
		else:
			self.x += 8
	
	def is_off_screen(self, left, right):
		return self.x < left - 20 or self.x > right + 20
	
	def void_this(self):
		self.expired = True
		
	