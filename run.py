import math
import os
import random
import re
import time

from collections import deque

import pygame
from pygame.locals import *




########################
## source\functions.py
########################
def max(a, b):
	if a > b:
		return a
	return b

def min(a, b):
	if a < b:
		return a
	return b

def ensure_range(x, lower, upper):
	return max(lower, min(upper, x))

def trim(string):
	if string == None or string == '':
		return ''
	
	whitespace = ' \n\r\t'
	index = 0
	while index < len(string):
		if string[index] in whitespace:
			index += 1
		else:
			break
	string = string[index:]
	
	index = len(string) - 1
	while index > 0:
		if string[index] in whitespace:
			index -= 1
		else:
			break
	
	string = string[:index + 1]
	return string

def get_text(string):
	return _text_printer.get_rendered_text(string)

def clear_text_cache():
	_text_printer.clear_cache()


########################
## source\ImageLibrary.py
########################
class ImageLibrary:
	
	def __init__(self):
		self.images = { }
	
	def Get(self, name):
		
		if not (name in self.images.keys()):
			filename = 'images' + os.sep + name.replace('/', os.sep)
			self.images[name] = pygame.image.load(filename)
		return self.images[name]




########################
## source\Input\InputEvent.py
########################
class InputEvent:
	def __init__(self, key, down):
		self.key = key
		self.down = down
		self.up = not down



########################
## source\Input\InputModel.py
########################

class InputModel:
	def __init__(self):
		self.keys = {
			'up' : False,
			'down' : False,
			'left' : False,
			'right' : False,
			'A' : False,
			'B' : False,
			'X' : False,
			'Y' : False,
			'start' : False,
			'L' : False,
			'R' : False
			}
		self.sources = [KeyboardInputSource()]
		
		#TODO: detect joysticks
		#TODO: set automated input to overtake KeyboardInputSource for automated gameplay cutscenes
	
	def get_input(self, pygame_events):
		inputevents = []
		for source in self.sources:
			inputevents += source.process_events(pygame_events)
			for event in inputevents:
				self.keys[event.key] = event.down
				
		return inputevents
	
	def is_key_pressed(self, key):
		return self.keys[key]




########################
## source\Input\KeyboardInputSource.py
########################

class KeyboardInputSource:
	def __init__(self):
		self.keymap = {
			K_UP : 'up',
			K_DOWN : 'down',
			K_LEFT : 'left',
			K_RIGHT : 'right',
			K_SPACE : 'B',
			K_z : 'Y',
			K_x : 'A',
			K_m : 'X',
			K_RETURN : 'start',
			K_1 : 'L',
			K_2 : 'R'
			}
	
	def process_events(self, pygame_events):
		events = []
		for event in pygame_events:
			if event.type == KEYDOWN or event.type == KEYUP:
				if event.key in self.keymap.keys():
					events.append(InputEvent(self.keymap[event.key], event.type == KEYDOWN))
		return events
		


########################
## source\SavedGame.py
########################
class SavedGame:
	
	def __init__(self, slot_num):
		self.path = 'saved' + os.sep + 'slot_' + str(slot_num) + '.txt'
		self.slot = slot_num
		
		if os.path.exists(self.path):
			self.values = self.read_slot_file(self.path)
		else:
			self.values = {
			'name' : '',
			'saved' : 0
			}
	
	def read_slot_file(self, path):
		c = open(path, 'rt')
		lines = c.read().split('\n')
		c.close()
		
		values = {}
		for line in lines:
			line = trim(line)
			
			if line != '':
				is_int = line[0] == '#'
				if is_int:
					line = line[1:]
				parts = line.split(':')
				key = parts[0]
				value = ':'.join(parts[1:])
				if is_int:
					value = int(value)
				values[key] = value
		return values

	def save_to_file(self):
		output = []
		for key in self.values.keys():
			name = key
			value = self.values[key]
			if type(value) == type(1):
				name = "#" + name
				value = str(value)
			
			output.append(name + ':' + value)
		
		c = open(self.path, 'wt')
		c.write('\n'.join(output))
		c.close()
	
	def save_value(self, name, value):
		self.values[name] = value
	
	def get_value(self, name):
		if name in self.values.keys():
			return self.values[name]
		return None

class SavedState:
	def __init__(self):
		self.active_saved_game = None
		self.saved_games = []
		
		for slot_num in (1, 2, 3):
			self.saved_games.append(SavedGame(slot_num))
	
	def active_game(self):
		return self.active_saved_game
	
	def set_active_game(self, slot_num):
		self.active_saved_game = self.saved_games[slot_num - 1]
	
	def get_saved_game(self, slot_num):
		return self.saved_games[slot_num - 1]
	
	def erase_game(self, slot_num):
		game = self.get_saved_game(slot_num)
		if game.get_value('saved') == 1:
			proxy_game = SavedGame(4) # does not exist
			game.values = proxy_game.values
			game.save_to_file()
	
	def copy_game(self, slot_from, slot_to):
		game_from = self.get_saved_game(slot_from)
		game_to = self.get_saved_game(slot_to)
		game_to.values = game_from.values
		game_to.save_to_file()
		
		# now it's a reference to the same dictionary instance but the files are correct
		# clear instance and re-instantiate one so the dictionary instances are unique
		
		self.saved_games[slot_to - 1] = SavedGame(slot_to)
		
		




########################
## source\Scenes\CutSceneScene.py
########################
class CutSceneScene:
	def __init__(self, name):
		self.next = self
		self.counter = 0
		self.script = SceneStateMachine(name)
		self.scene = None
		
		self.SetScene(self.script.Next())

	def SetScene(self, scn):
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
			return
		
		frame = self.scene
		screen.blit(images.Get(frame.image), (frame.coords))
   
	def Update(self):
		self.counter += 1
	

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


########################
## source\Scenes\LoadScene.py
########################
class LoadScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
	
	def ProcessInput(self, events):
		pass
		
	def Render(self, screen):
		screen.blit(images.Get('load_splash.png'), (0, 0))
	
	def Update(self):
		self.counter += 1
		
		if self.counter > 2: #don't check this in
			self.next = TitleScene()


########################
## source\Scenes\MapScene.py
########################
class MapScene:
	def __init__(self, world_num):
		self.counter = 0
		self.next = self
		self.world_num = world_num
		self.location = ''
		self.nodes = self._read_map_file()
		#TODO: set initial location from save game
		self.bg_image = None
		self.destination = self.location
		self.move_counter = 0
		
	def Update(self):
		self.counter += 1
		
		if self.destination != self.location:
			self.move_counter += 1
			
			if self.move_counter >= 15:
				self.move_counter = 0
				self.location = self.destination
		
	
	def Render(self, screen):
		
		if self.bg_image == None:
			self.bg_image = self.generate_map()
		
		screen.blit(self.bg_image, (0, 0))
		
		character = images.Get('sprites/EvilWizardDude.png') #TODO: change this from the wizard
		start_node = self.nodes[self.location]
		end_node = self.nodes[self.destination]
		start_x = start_node['x']
		start_y = start_node['y']
		end_x = end_node['x']
		end_y = end_node['y']
		x = int(start_x * (15 - self.move_counter) / 15.0 + end_x * self.move_counter / 15.0 - character.get_width() / 2)
		y = int(start_y * (15 - self.move_counter) / 15.0 + end_y * self.move_counter / 15.0 - character.get_height() / 2)
		screen.blit(character, (x, y))
	
	def ProcessInput(self, events):
		for event in events:
			if self.move_counter == 0:
				node = self.nodes[self.location]
				if event.down and event.key in ('left','right','down','up'):
					for connection in node['connections']:
						if connection[1] == event.key:
							self.destination = connection[0]
							break
				elif event.down and event.key in ('start', 'B', 'A'):
					self.next = PlayScreen(str(self.world_num) + '_' + self.location) # TODO: actually initialize this to a level splash screen
	
	def generate_map(self):
		original = images.Get('maps/world_' + str(self.world_num) + '.png')
		background = pygame.Surface((256, 224))
		background.blit(original, (0, 0))
		
		nodes = self.nodes
		
		color = (255, 255, 255)
		complete_color = (255, 255, 0)
		incomplete_color = (255, 0, 0)
		for start in nodes.keys():
			start_x = nodes[start]['x']
			start_y = nodes[start]['y']
			
			for end in nodes[start]['connections']:
				end_x = nodes[end[0]]['x']
				end_y = nodes[end[0]]['y']
				
				for i in range(50):
					x = int(start_x * i / 50.0 + end_x * (50 - i) / 50.0)
					y = int(start_y * i / 50.0 + end_y * (50 - i) / 50.0)
					pygame.draw.circle(background, color, (x, y), 5)
		for node in nodes.values():
			color = incomplete_color
			if node['completed'] == 1:
				color = complete_color
			pygame.draw.circle(background, (0, 0, 0), (node['x'], node['y']), 9)
			pygame.draw.circle(background, color, (node['x'], node['y']), 7)
			
		return background
	
	def _read_map_file(self):
		c = open(os.path.join('levels', 'world_map', 'world_' + str(self.world_num) + '.txt'), 'rt')
		lines = c.read().split('\n')
		c.close()
		nodes = {}
		connections = False
		for line in lines:
			line = trim(line)
			if not connections:
				if line == '#connections':
					connections = True
				else:
					parts = line.split('\t')
					id = parts[0]
					if self.location == '': #TODO: remove this when start location is loaded from saved game
						self.location = id
					coords = parts[1].split(',')
					x = int(coords[0])
					y = int(coords[1])
					nodes[id] = {
						'id' : id,
						'x' : x,
						'y' : y,
						'connections' : [],
						'completed' : (games.active_game().get_value('finished_world' + str(self.world_num) + '_' + id) == 1)
					}
			else:
				parts = line.split('\t')
				left = parts[0]
				right = parts[1]
				direction = parts[2]
				nodes[left]['connections'].append((right, direction))
				nodes[right]['connections'].append((left, self._swap_direction(direction)))
				
		return nodes
	
	def _swap_direction(self, d):
		if d == 'right': return 'left'
		if d == 'left' : return 'right'
		if d == 'down' : return 'up'
		if d == 'up'   : return 'down'


########################
## source\Scenes\NameEntry\NameEntryScene.py
########################

class NameEntryScene:
	
	def __init__(self, game):
		self.next = self
		self.counter = 0
		self.cursor_x = 0
		self.cursor_y = 0
		self.mode = 'selection' # 'copy' or 'erase'
		self.text_entry = ''
		self.game = game
		
	def ProcessInput(self, events):
		
		for event in events:
			if event.down:
				if event.key == 'up':
					self.cursor_y = max(0, self.cursor_y - 1)
				elif event.key == 'down':
					self.cursor_y = min(5, self.cursor_y + 1)
				elif event.key == 'left' and self.cursor_y < 5:
					self.cursor_x = max(0, self.cursor_x - 1)
				elif event.key == 'right' and self.cursor_y < 5:
					self.cursor_x = min(7, self.cursor_x + 1)
				elif event.key == 'start' or event.key == 'A':
					
					if len(self.text_entry) < 10:
						char = self.current_character()
						name = self.text_entry
						if char == None:
							if len(name) > 0:
								self.game.save_value('name', name)
								self.game.save_value('saved', 1)
								self.game.save_to_file()
								self.next = SelectGameScene()
							else:
								# TODO: play error sound
								pass
						else:	
							self.text_entry += char
					
					
				elif event.key == 'B':
					self.text_entry = self.text_entry[:-1]
		
					
		
	def Render(self, screen):
		
		cursor_coords = self._get_coords(self.cursor_x, self.cursor_y)
		
		name = self.text_entry
		if int(self.counter / 15) % 2 == 1:
			name += '_'
		
		screen.blit(get_text(name), (10, 10))
		
		pygame.draw.circle(screen, (120, 120, 120), (cursor_coords[0] + 4, cursor_coords[1] + 4), 7)
		
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .,-'
		
		for x in range(6):
			for y in range(5):
				index = y * 6 + x
				letter = alphabet[index]
				screen.blit(get_text(letter), self._get_coords(x, y))
		
		numbers = '1234567890'
		
		for x in (0, 1):
			for y in range(5):
				index = y * 2 + x
				number = numbers[index]
				screen.blit(get_text(number), self._get_coords(x + 6, y))
		
		screen.blit(get_text("END"), self._get_coords(0, 5))
		
	def _get_coords(self, x, y):
		x_left = 20
		y_top = 50
		
		new_x = x_left + x * 15
		new_y = y_top + y * 15
		
		if (x > 5):
			new_x += 10
		
		if y == 5:
			new_x = x_left + 50
		
		return (new_x, new_y)
	
	def Update(self):
		self.counter += 1
	
	def current_character(self):
		if self.cursor_y == 5:
			return None
		
		if self.cursor_x < 6:
			alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .,-'
			index = self.cursor_x + self.cursor_y * 6
			return alphabet[index]
		
		else:
			x = self.cursor_x - 6
			index = x + self.cursor_y * 2
			numbers = '1234567890'
			return numbers[index]
			
		
		


########################
## source\Scenes\NameEntry\SelectGameScene.py
########################

class SelectGameScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
		self.cursor_index = 0
		self.mode = 'selection' # 'copy' or 'erase' or paste
		self.text_entry = ''
		self.copy_from = 0
		
		
		
	def ProcessInput(self, events):
		
		enter_pressed = False
		
		for event in events:
			if event.down:
				if event.key == 'up':
					self.cursor_index -= 1
				elif event.key == 'down':
					self.cursor_index += 1
				elif event.key == 'start' or event.key == 'A' or event.key == 'B':
					enter_pressed = True
		if self.cursor_index < 0:
			self.cursor_index = 0
		elif self.cursor_index > 4:
			self.cursor_index = 4
		
		
		if enter_pressed:
			if self.cursor_index == 4:
				if self.mode == 'erase':
					self.mode = 'selection'
				else:
					self.mode = 'erase'
			elif self.cursor_index == 3:
				if self.mode == 'copy' or self.mode == 'paste':
					self.mode = 'selection'
				else:
					self.mode = 'copy'
			else: # 0, 1, 2
				if self.mode == 'selection':
					game = games.get_saved_game(self.cursor_index + 1)
					if game.get_value('saved') == 0:
						self.next = NameEntryScene(game)
					else:
						games.set_active_game(self.cursor_index + 1)
						self.next = MapScene(1) # TODO: actually read last level completed from file
				elif self.mode == 'erase':
					games.erase_game(self.cursor_index + 1)
					self.mode = 'selection'
				elif self.mode == 'copy':
					self.copy_from = self.cursor_index + 1
					self.mode = 'paste'
				elif self.mode == 'paste':
					if self.copy_from == self.cursor_index + 1:
						self.mode = 'copy'
					else:
						self.mode = 'selection'
						games.copy_game(self.copy_from, self.cursor_index + 1)
					
				
	
	def Render(self, screen):
		
		screen.blit(get_text('SELECT GAME'), (10, 10))
		
		x_offset = 10
		
		for slot in (1, 2, 3):
			game = games.get_saved_game(slot)
			is_empty = game.get_value('saved') == 0
			name = game.get_value('name')
			slot_label = get_text('SLOT ' + str(slot) + ': ')
			y = 30 + slot * 16
			mid_y = y + int(slot_label.get_height() / 2)
			
			screen.blit(slot_label, (x_offset, y))
			if is_empty:
				name = get_text('(EMPTY)')
			else:
				name = get_text(name)
			screen.blit(name, (x_offset + slot_label.get_width(), y))
			
			if self.cursor_index + 1 == slot:
				self._draw_cursor_at(x_offset - 5, mid_y)
				
			if self.mode == 'paste' and self.copy_from == slot:
				self._draw_cursor_at(x_offset - 5, mid_y, True)
		
		# copy game
		screen.blit(get_text('COPY GAME'), (x_offset, 120))
		if self.cursor_index == 3:
			self._draw_cursor_at(x_offset - 5, 120 + 4)
		
		# erase game
		screen.blit(get_text('ERASE GAME'), (x_offset, 140))
		if self.cursor_index == 4:
			self._draw_cursor_at(x_offset - 5, 140 + 4)
			
	def _draw_cursor_at(self, x, y, copy_from = False):
		color = (120, 120, 120)
		if copy_from:
			color = (128, 0, 128)
		elif self.mode == 'copy' or self.mode == 'paste':
			color = (0, 0, 255)
		elif self.mode == 'erase':
			color = (255, 0, 0)
		pygame.draw.circle(screen, color, (x, y), 3)
		
		
	def Update(self):
		self.counter += 1
		


########################
## source\Scenes\PlayScene.py
########################
class PlayScreen:
	def __init__(self, level):
		self.counter = 0
		self.next = self
		self.level_id = level
		wibbly_wobbly = False
	
	def ProcessInput(self, events):
		pass
	
	def Update(self):
		pass
	
	def Render(self, screen):
		pass
	
	


########################
## source\Scenes\TitleScene.py
########################
class TitleScene:
	
	def __init__(self):
		self.next = self
		self.counter = 0
	
	def ProcessInput(self, events):
		for event in events:
			if event.key == 'start':
				self.next = SelectGameScene()
			elif event.key == 'L':
				self.next = CutSceneScene('demo')
	
	def Render(self, screen):
		screen.blit(images.Get('title.png'), (0, 0))
	
	def Update(self):
		self.counter += 1


########################
## source\SoundManager.py
########################
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




########################
## source\Soundtrack.py
########################
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
	
	def Fadeout(self, endQueue = True, time = 2000):
		pygame.mixer.music.fadeout(time)
		if endQueue:
			self.playQueue = None

class PlayQueue:
	def __init__(self, lst = None):
		self.position = 0
		self.songList = []
		self.loopLast = False
		
		if lst:
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




########################
## source\TextEngine\TextPrinter.py
########################
class TextPrinter:
	
	def __init__(self):
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		self.space_width = 8
		
		self.images = {
			' ' : pygame.Surface((self.space_width, 1), SRCALPHA)
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
			self.images[char] = images.Get('text/punctuation/' + file + '.png')
			
	def get_rendered_text(self, string):
		
		if string == None or len(string) == 0:
			string = ' '
		
		if string in self.text_cache.keys():
			return self.text_cache[string]
		
		surface = pygame.Surface(self.calc_size(string), SRCALPHA)
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
			max_height = max(max_height, img.get_height())
		return (width, max_height)
	
	def get_image_for_char(self, char):
		if not (char in self.images.keys()):
			char = '?'
		return self.images[char]
	
	def clear_cache(self):
		self.text_cache = {}
		




########################
## source\ImageLibrary.py (static)
########################

images = ImageLibrary()

########################
## source\Input\InputModel.py (static)
########################


input = InputModel()

########################
## source\SavedGame.py (static)
########################

games = SavedState()

########################
## source\SoundManager.py (static)
########################

soundMgr = SoundManager()

########################
## source\Soundtrack.py (static)
########################

MUSICEND = USEREVENT
MUSICTIME = USEREVENT + 1

soundtrack = Soundtrack()

########################
## source\TextEngine\TextPrinter.py (static)
########################


_text_printer = TextPrinter()
# handy functions
def max(a, b):
	if a > b:
		return a
	return b

def min(a, b):
	if a < b:
		return a
	return b

def ensure_range(x, lower, upper):
	return max(lower, min(upper, x))

def trim(string):
	if string == None or string == '':
		return ''
	
	whitespace = ' \n\r\t'
	index = 0
	while index < len(string):
		if string[index] in whitespace:
			index += 1
		else:
			break
	string = string[index:]
	
	index = len(string) - 1
	while index > 0:
		if string[index] in whitespace:
			index -= 1
		else:
			break
	
	string = string[:index + 1]
	return string

def get_text(string):
	return _text_printer.get_rendered_text(string)

def clear_text_cache():
	_text_printer.clear_cache()
####################
# main.py
####################
pygame.init()

fullscreen = False

output_screen = pygame.display.set_mode((800, 600))

screen = pygame.Surface((256, 224))

counter = 0

scene = LoadScene()

while scene != None:
	
	start = time.time()
	
	events = []
	for event in pygame.event.get():
		if event.type == MUSICEND:
			soundtrack.HandleEvent(event)
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			scene = None
		elif event.type == KEYDOWN and event.key == K_f:
			fullscreen = not fullscreen
			if fullscreen:
				output_screen = pygame.display.set_mode((800, 600), FULLSCREEN)
			else:
				output_screen = pygame.display.set_mode((800, 600))
		else:
			events.append(event)
	
	if scene == None:
		break
	
	scene.ProcessInput(input.get_input(events))
	
	scene.Update()
	
	screen.fill((0,0,0))
	
	scene.Render(screen)
	
	pygame.transform.scale(screen, (800, 600), output_screen)
	
	if scene != scene.next:
		clear_text_cache()
		scene = scene.next
	
	end = time.time()
	
	ellapsed = end - start
	framerate = 1.0 / 30
	
	delay = framerate - ellapsed
	if delay > 0:
		time.sleep(delay)
	else:
		# remove me before release
		print('framerate dropping ('+str(counter)+')')
	pygame.display.flip()
	
	counter += 1

pygame.quit()