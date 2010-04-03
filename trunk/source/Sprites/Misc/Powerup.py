class Powerup(Sprite):
	
	def __init__(self, x, y, type):
		# types:
		# little_recharge
		# big_recharge
		# wand_1, ... wand_4
		# mumblefoo_piece1
		# mumblefoo_piece2
		# invincibility
		self.lifetime = 0
		Sprite.__init__(self, x, y)
		self.type = type
		self.width = 16
		self.height = 16
		
		if type in ('little_recharge', 'mumblefoo_piece1', 'mumblefoo_piece2'):
			self.width = 8
			self.height = 8
		
		self.confined_to_scene = True
		self.is_powerup = True
		self.taken = False
		
	def get_wand_id(self):
		if self.type[-1] == '1':
			return 'ice'
		if self.type[-1] == '2':
			return 'fire'
		if self.type[-1] == '3':
			return 'lightning'
		if self.type[-1] == '4':
			return 'charge'
	
	def draw(self, surface, is_moving, counter, camera_offset):
		
		if self.taken:
			return
			
		if self.type[:5] == 'mumbl':
			file = 'sprites/mumblefoo/mumblefoo' + str(int(counter % 8)) + '.png'
		elif self.type[:4] == 'wand':
			id = self.get_wand_id()
			file = 'wands/' + id + '.png'
		else:
			file = 'powerups/' + self.type + '_' + str(int(counter % 4)) + '.png'
		img = images.Get(file)
		
		xy = self.get_top_left()
		x = xy[0] - camera_offset[0]
		y = xy[1] - camera_offset[1]
		
		surface.blit(img, (x, y))
	
	
	def update(self, playScene):
		self.lifetime += 1

	def collected(self, playScene):
		if self.type == 'big_recharge':
			wandStatus.RechargeMagic(True)
		elif self.type == 'little_recharge':
			wandStatus.RechargeMagic(False)
		elif self.type[:5] == 'mumbl':
			if self.type[-1] == '1':
				games.active_game().save_value('finished_world1_5', 1)
				jukebox.PlayVictory()
				playScene.text_triggers['timer'].append(
				(0, "You have collected a piece \n of your soul! \n  \n  You recall seeing another \n piece fly towards the desert.", TransitionScene(self, MapScene(1, '5', 'next'), 'fadeout', 30)))
			if self.type[-1] == '2':
				games.active_game().save_value('finished_world2_5', 1)
				jukebox.PlayVictory()
				playScene.text_triggers['timer'].append(
				(0, "You have collected a piece \n of your soul!\n \n You recall the final \n piece flying somewhere over\n the mountains towards your\n Mentor's castle. Maybe he's \n already found it.", TransitionScene(self, MapScene(2, '5', 'next'), 'fadeout', 30)))
					
			self.taken = True
		elif self.type[:4] == 'wand':
			id = self.get_wand_id()
			games.active_game().save_value('wand_' + self.type[-1], 1)
			
			playScene.text_triggers['timer'].append(
			(0,
			"You found the \n " + id.upper() + ' wand!', None)
			)	