class CutSceneScene:
	def __init__(self, name, nextScene):
		self.next = self
		self.nextScene = nextScene
		self.counter = 0
		self.script = SceneStateMachine(name)
		self.scene = None
		self.oldScreen = None
		self.sceneStartTime = None
		
		self.SetScene(self.script.Next())

	def SetScene(self, scn):
		self.sceneStartTime = time.time()
		self.text_counter = 1
		
		self.scene = scn
		if not scn:
			return

		music = scn.music
		if 'stop' == music:
			soundtrack.Stop()
		elif 'fadeout' == music:
			soundtrack.Fadeout()
		elif music:
			bg = PlayQueue()
			bg.SetLoopLast(True)
			
			tracks = music.split(',')
			for t in tracks:
				bg.AddTrack(t.strip())
			
			soundtrack.SetQueue(bg)
			soundtrack.Play()

	def ProcessInput(self, events):
		for event in events:
			if event.down and event.key == 'start':
				self.SetScene(self.script.Next())
				
	def Render(self, screen):
		if not self.scene:
			if self.oldScreen != None:
				screen.blit(self.oldScreen, (0, 0))
			if self.next == self:
				self.next = TransitionScene(self, self.nextScene, 'fadeout', 30)
			return
		
		frame = self.scene
		if self.oldScreen:
			self.oldScreen.blit(images.Get(frame.image), (frame.coords))
			screen.blit(self.oldScreen, ((0,0)))
		else:
			screen.blit(images.Get(frame.image), (frame.coords))

		# save the image without the text
		self.oldScreen = screen.copy()
		
		if frame.text:
			text = frame.text
			if len(text) > self.text_counter:
				text = text[:self.text_counter]
			elif int((self.counter / 10) % 2) == 0:
				text += '~'
			txtList = text.split('\\n')
			yOffset = 170
			i = 0
			for txt in txtList:
				t = get_text(frame.text)
				
				screen.blit(get_text(txt), (10, yOffset + 18 * i))
				i += 1
		

  
	def Update(self):
		scn = self.scene
		self.text_counter += 1
		
		if scn and scn.transition and scn.transition == 'timed':
			passedTime = 1000 * (time.time() - self.sceneStartTime)
			if passedTime > scn.delay:
				self.SetScene(self.script.Next())
		
		self.counter += 1
	

class Frame:
	def __init__(self):
		self.image = None
		self.coords = None
		self.text = None
		self.music = None
		self.transition = None
		self.delay = None
	
	def __str__(self):
		ret =  'frame: {\n'
		ret += '    ' + str(self.image) + '\n'
		ret += '    ' + str(self.coords) + '\n'
		ret += '    ' + str(self.text) + '\n'
		ret += '    ' + str(self.music) + '\n'
		ret += '    ' + str(self.transition) + '\n'
		ret += '    ' + str(self.delay) + '\n'
		ret += '}'
		return ret


class SceneStateMachine:
	def __init__(self, script):
		self.frameSet = self.parseScript(script + '.scn');

	def Next(self):
		if 0 == len(self.frameSet):
			return None
		return self.frameSet.popleft()
	
	def parseScript(self, script):
		reFrame = re.compile('^\[frame\]')
		reEnd = re.compile('^\[end\]')
		reCoords = re.compile('^\[coords: (\d+),(\d+)\]')
		reImage = re.compile('^\[image:(.*)\]')
		reText = re.compile('^\[text:(.*)\]')
		reMusic = re.compile('^\[music:(.*)\]')
		reTransition = re.compile('^\[transition:(.*)\]')
		reTimedTransition = re.compile('^timed:(.*)$')
		
		frameSet = []
	
		path = 'levels' + os.sep + 'scripts' + os.sep + script.replace('/', os.sep)
		if not os.path.exists(path):
			raise Exception("Could not find script " + script)
		
		scr = open(path)
		
		frame = None
		for line in scr:
			line = line.strip()
			
			if reFrame.match(line):
				if frame:
					frameSet.append(frame)
				frame = Frame();
				continue
			
			if reEnd.match(line):
				if frame:
					frameSet.append(frame)
				break
			
			m = reCoords.match(line)
			if m:
				frame.coords = (int(m.group(1)), int(m.group(2)))
				continue
			
			m = reImage.match(line)
			if m:
				img = m.group(1).strip()
				frame.image = img
				continue
			
			m = reText.match(line)
			if m:
				txt = m.group(1).strip()
				frame.text = txt
				continue
			
			m = reMusic.match(line)
			if m:
				music = m.group(1).strip()
				frame.music = music
				continue

			m = reTransition.match(line)
			if m:
				tran = m.group(1).strip()
				m = reTimedTransition.match(tran)
				if m:
					tran = 'timed'
					frame.delay = int(m.group(1).strip())
				frame.transition = tran
				continue
			
			if line == '':
				continue
			
			else:
				raise Exception("Could not match " + line)
		
		scr.close()
		return deque(frameSet)