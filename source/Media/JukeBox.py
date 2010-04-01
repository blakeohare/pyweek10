class JukeBox:
	
	def __init__(self):
		
		pygame.mixer.init()
		
		self.sounds = {}
		sounds_folder = 'media' + os.sep + 'sound'
		for file in os.listdir(sounds_folder):
			if file.endswith('.wav'):
				name = file[:-4]
				path = sounds_folder + os.sep + file
				self.sounds[name] = pygame.mixer.Sound(path)
	
		self.next_song = None
		self.next_song_loops = 0
		self.now_playing = None
		self.fading = False
	
		
	def Update(self):
		if self.fading:
			if not pygame.mixer.music.get_busy():
				self.fading = False
		
		if not self.fading and self.next_song != None:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(self.next_song)
			for tries in range(5): # >:( sometimes I really hate PyGame
				pygame.mixer.music.play(self.next_song_loops)
				
				time.sleep(0.03)
				
				if pygame.mixer.get_busy():
					break
				
				
					
			self.next_song = None
			self.next_song_loops = 0
		
	
	
	def PlaySound(self, name):
		if name in self.sounds.keys():
			self.sounds[name].play()
		else:
			print("WARNING: unknown sound file: " + name + '.wav')
	
	def _play_song_once(self, file):
		self._play_song(file, 0)
		
	def _play_song_looping(self, file):
		self._play_song(file, -1)
		
	def _play_song(self, file, loop):
		if self.now_playing != file:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.fadeout(100) # no abrupt cut-offs
				self.fading = True
			self.next_song = 'media' + os.sep + 'music' + os.sep + file + '.mp3'
			self.next_song_loops = loop
			self.now_playing = file
		
	def FadeOut(self, seconds):
		self.now_playing = None
		pygame.mixer.music.fadeout(int(seconds * 1000))
	
	def Stop(self):
		self.now_playing = None
		pygame.mixer.music.fadeout(100)
	
	# specific songs
	def PlayTitle(self):
		self._play_song_once('opening_fanfare')
	
	def PlayDeath(self):
		self._play_song_once('death')
	
	def PlayMapMusic(self):
		self._play_song_looping('maploop')
	
	def PlayLevelMusic(self, music):
		if music == 'overworld1':
			self._play_song_looping('windyday')
		else:
			print("WARNING: unrecognized song in level file")
		
#STATIC

jukebox = JukeBox()