class CutSceneScene:
	def __init__(self):
		self.next = self
		self.counter = 0
		self.scene = None
		self.script = None
		
		self.SetScript('demo.scn')

	def ProcessInput(self, events):
		for event in events:
			if event.down and event.key == 'start':
				self.scene = self.script.Next()
   
	def Render(self, screen):
		if not self.scene:
			return
		
		frame = self.scene
		screen.blit(images.Get(frame.image), (frame.coords))
   
	def Update(self):
		self.counter += 1
	
	def SetScript(self, sceneScriptFile):
		self.script = SceneStateMachine(sceneScriptFile)
		self.scene = self.script.Next()


class Frame:
	def __init__(self):
		self.image = None
		self.coords = None
		self.text = None
		self.music = None
		self.transition = None
	
	def __str__(self):
		ret =  'frame: {\n'
		ret += '    ' + str(self.image) + '\n'
		ret += '    ' + str(self.coords) + '\n'
		ret += '    ' + str(self.text) + '\n'
		ret += '    ' + str(self.music) + '\n'
		ret += '    ' + str(self.transition) + '\n'
		ret += '}'
		return ret


class SceneStateMachine:
	def __init__(self, script):
		self.frameSet = self.parseScript(script);

	def Next(self):
		return self.frameSet.popleft()
	
	def parseScript(self, script):
		reFrame = re.compile('^\[frame\]')
		reEnd = re.compile('^\[end\]')
		reCoords = re.compile('^\[coords: (\d+),(\d+)\]')
		reImage = re.compile('^\[image:(.*)\]')
		reText = re.compile('^\[text:(.*)\]')
		reMusic = re.compile('^\[music:(.*)\]')
		reTransition = re.compile('^\[transition:(.*)\]')
		
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
				frame.transition = tran
				continue
			
			if line == '':
				continue
			
			else:
				raise Exception("Could not match " + line)
		
		scr.close()
		return deque(frameSet)