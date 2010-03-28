class Soundtrack:
	def __init__(self):
		self.playQueue = None
		self.paused = False
		
		pygame.mixer.music.set_endevent(MUSICEND)
		
	def HandleEvent(self, event):
		pq = self.playQueue
		if not pq:
			return
		
		if event.type == MUSICTIME:
			pass
		
		if event.type == MUSICEND:
			nextTrack = pq.Next()
			if nextTrack:
				pq.Advance()
				self.Play()
			elif pq.LoopLast():
				self.Loop()
	
	def GetNewQueue(self):
		return PlayQueue()

	def SetQueue(self, q):
		self.playQueue = q

	def Play(self):
		self.Loop(0)

	def Loop(self, num = -1):
		pq = self.playQueue
		if not pq:
			raise Exception("Must set PlayQueue before playing music")
		
		if self.paused:
			self.Unpause()
			return
		
		pygame.mixer.music.load(pq.CurrentTrack())
		pygame.mixer.music.play(num)
	
	def Pause(self):
		self.paused = True
		pygame.mixer.music.pause()
	
	def Unpause(self):
		self.paused = False
		pygame.mixer.music.unpause()
	
	def Stop(self):
		pygame.mixer.music.stop()
	
	def Fadeout(self, time = 2000):
		pygame.mixer.music.fadeout(time)

class PlayQueue:
	def __init__(self, lst = None):
		self.position = 0
		self.songList = []
		self.loopLast = False
		
		for element in lst:
			self.AddTrack(element)
	
	def NameToFile(self, name):
		f = 'media' + os.sep + 'music' + os.sep + name.replace('/', os.sep)
		if os.path.exists(f):
			return f
		
		raise Exception("Could not find file " + f)

	def LoopLast(self):
		return self.loopLast

	def SetLoopLast(self, loop):
		self.loopLast = loop
	
	def AddTrack(self, track):
		f = self.NameToFile(track)
		self.songList.append(f)
	
	def Tracks(self):
		return self.songList

	def Advance(self):
		self.position += 1
	
	def CurrentTrack(self):
		p = self.position
		sl = self.songList
		
		if p < 0 or p >= len(sl):
			return None
		
		return sl[p]
	
	def Next(self):
		p = self.position + 1
		sl = self.songList
		
		if p < 0 or p >= len(sl):
			return None
		
		return sl[p]
	
	def Previous(self):
		p = self.position -1
		sl = self.songList
		
		if p < 0 or p >= len(sl):
			return None
		
		return sl[p]

#STATIC
MUSICEND = USEREVENT
MUSICTIME = USEREVENT + 1

soundtrack = Soundtrack()