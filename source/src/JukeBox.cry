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
		self.previous_song = None
		self.level_music = None
		self.counter = 0
		
	def Update(self):
		self.counter += 1
		if self.fading:
			if not pygame.mixer.music.get_busy():
				self.fading = False
		
		if not self.fading and self.next_song != None:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(self.next_song)
			for tries in range(5): # >:( sometimes I really hate PyGame
				pygame.mixer.music.play(self.next_song_loops)
				
				time.sleep(0.01)
				
				if pygame.mixer.get_busy():
					break
				
				
					
			self.next_song = None
			self.next_song_loops = 0
		
	
	
	def PlaySound(self, name):
		if name == '':
			return
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
				self.previous_song = self.now_playing
			else:
				self.previous_song = None
		self.next_song = 'media' + os.sep + 'music' + os.sep + file + '.mp3'
		#print self.counter, 'next_song_is ', self.next_song
		self.next_song_loops = loop
		self.now_playing = file
		
	def FadeOut(self, seconds):
		self.now_playing = None
		pygame.mixer.music.fadeout(int(seconds * 1000))
	
	def Stop(self):
		self.now_playing = None
		pygame.mixer.music.fadeout(100)
	
	def MakeQuiet(self):
		pygame.mixer.music.set_volume(0.5)
	
	def MakeLoud(self):
		pygame.mixer.music.set_volume(1.0)
	
	# specific songs
	def PlayTitle(self):
		self._play_song_once('opening_fanfare')
	
	def PlayDeath(self):
		self._play_song_once('death')
	
	def PlayVictory(self):
		self._play_song_once('fanfare')
		
	def PlayMapMusic(self):
		self._play_song_looping('maploop')
	
	def PlayCredits(self):
		self._play_song_looping('credits')
	
	def PlayLevelMusic(self, music):
		self.level_music = music
		self.previous_song = music
		if music == 'overworld1' or music == '':
			self._play_song_looping('windyday')
		elif music == 'overworld2':
			self._play_song_looping('overworld2')
		elif music == 'icy':
			self._play_song_looping('icy')
		elif music == 'castle':
			self._play_song_looping('darkwizard')
		elif music == 'desert':
			self._play_song_looping('desert')
		elif music == 'boss':
			self._play_song_looping('boss')
		elif music == 'water':
			self._play_song_looping('aquatic assault')
		elif music == 'cavern':
			self._play_song_looping('cave')
		else:
			print("WARNING: unrecognized song in level file")
	
	def MumblefooDropped(self):
		self._play_song_looping('watchout')
	
	def MumblefooPickedUp(self):
		if self.level_music != None:
			self.PlayLevelMusic(self.level_music)
		else:
			self.Stop()
		
#STATIC

jukebox = JukeBox()