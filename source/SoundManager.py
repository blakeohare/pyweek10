class SoundManager:
	def __init__(self):
		self.clips = {}

	def Get(self, name):
		file = 'media' + os.sep + 'music' + os.sep + name.replace('/', os.sep)
		
		if not (name in self.clips.keys()):
			self.clips[name] = pygame.mixer.Sound(file)
		
		return self.clips[name]
	
	def NameToFile(self, name):
		f = 'media' + os.sep + 'music' + os.sep + name.replace('/', os.sep)
		if os.path.exists(f):
			return f
		
		raise Exception("Could not find file " + f)
	
	def Load(self, name):
		file = self.NameToFile(name)
		
		if not (name in self.clips.keys()):
			self.clips[name] = pygame.mixer.Sound(file)
		pygame.mixer.music.load(file)

	def Queue(self, name):
		file = self.NameToFile(name)
		
		pygame.mixer.music.queue(file)

	def Play(self):
		pygame.mixer.music.play()

class Song:
	def __init__(self, file, mgr):
		self.sound = pygame.mixer.Sound(file)
		self.mgr = mgr
	
	def Play(self):
		self.sound.Play()
	
	def Stop(self):
		self.sound.Stop
	
	def Loop(self, times = -1):
		self.sound.Play(times)

#STATIC
soundMgr = SoundManager()