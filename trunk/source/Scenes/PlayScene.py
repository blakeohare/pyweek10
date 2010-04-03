
class PlayScreen:
	def __init__(self, level, screen, start_location=None):
		self.counter = 0
		self.render_counter = 0
		
		self.next = self
		self.g = 1.4
		self.water_g = .2
		self.level_id = level
		
		self.screen_id = screen
		
		self.level_info = levels.get_level(self.level_id + screen)
		
		wibbly_wobbly = False
		
		start_loc = self.level_info.get_start_location(start_location)
		
		self.renderInventory = True
		
		self.target_vx = 0
		
		self.player = MainCharacter(start_loc[0] * 16, start_loc[1] * 16 + 1)
		self.enemies = self.level_info.get_enemies()
		self.powerups = []
		
		self.mumblefoo = None
		self.wibblywobbly = WibblyWobblyRenderer()
		self.wibblywobbly_counter = 0
	
		self.allow_enemy_edit = True #TODO: change this to false right before release
		self.enemy_edit_mode = False
		self.wand_cooldown = 0
		self.bullets = []
		camera_offset = self.get_real_camera_offset()
		self.camera_x = camera_offset[0] + 0.0
		self.camera_y = camera_offset[1] + 0.0
		
		self.wand_charge = 0
		
		self.other_sprites = []
		
		self.text_triggers = {
		'timer' : [],
		'soul_pickup' : None
		}
		if self.level_id == '0_1':
			self.text_triggers['timer'] = [
					(10, "Wow, I never realized how \n much misplacing a soul could \n make my mind and body go all \n wibbly wobbly. It seems one \n of the larger chunks fell into \n the bushes over there.", None)
					]
			self.text_triggers['soul_pickup'] = ("Phew, if I didn't pick that up \n sooner it may have been \n game over for me. \n I better be careful not to \n drop this again!", TransitionScene(self, MapScene(1, '1'), 'fadeout', 30))
			
			
			self.mumblefoo = SoulJar(230, 224 - 50, 0)
			self.wibblywobbly_counter = 60
			self.mumblefoo.vx = 0
			self.mumblefoo.vy = 0
		
		if self.level_id == '3_5' and self.screen_id == 'a':
			
			self.text_triggers['timer'] = [
					(1, "Curious, I don't recall his\ncastle being this gloomy. He\nmust have remodelled recently.", None)
					]
		
		if	games.active_game() != None:
			
			if games.active_game().get_value('wand_1') != 1 and self.level_id == '1_3' and self.screen_id == 'b':
				self.powerups.append(Powerup(88, 40, 'wand_1'))
			
			if games.active_game().get_value('wand_2') != 1 and self.level_id == '2_1' and self.screen_id == 'b':
				self.powerups.append(Powerup(90 + 9 * 16, 80, 'wand_2'))
			
			if games.active_game().get_value('wand_3') != 1 and self.level_id == '2_5' and self.screen_id == 'c':
				self.powerups.append(Powerup(152, 48, 'wand_3'))
			
			#TODO
			if games.active_game().get_value('wand_4') != 1 and self.level_id == '1_1' and self.screen_id == 'a':
				self.powerups.append(Powerup(130, 40, 'wand_4'))
			
			if self.level_id == '1_5' and self.screen_id == 'c':
				self.powerups.append(Powerup(14 * 16, 32, 'mumblefoo_piece1'))
			
			if self.level_id == '2_5' and self.screen_id == 'd':
				self.powerups.append(Powerup(31 * 16, 10 * 16, 'mumblefoo_piece2'))
			
			
			if self.level_id == '3_5' and self.screen_id == 'c':
				self.enemies.append(EnemyCornelius(220, 80))
			
		
	def get_sprites(self):
		
		sprites = []
		if self.mumblefoo != None:
			sprites.append(self.mumblefoo)
		sprites.append(self.player)
		sprites += self.powerups
		sprites += self.enemies
		sprites += self.other_sprites
		
		return sprites
	
	def get_real_camera_offset(self):
		width = self.level_info.get_width()
		height = self.level_info.get_height()
		x = self.player.x - 128
		y = self.player.y - 112
		x = max(min(x, width * 16 - 256), 0)
		y = max(min(y, height * 16 - 224), 0)
		return (x, y)
	
	def get_camera_offset(self):
		return (int(self.camera_x), int(self.camera_y))
	
	def update_camera(self):
		new = self.get_real_camera_offset()
		self.camera_x = (self.camera_x * 0.7 + new[0] * 0.3)
		self.camera_y = (self.camera_y * 0.7 + new[1] * 0.3)
		
	
	def get_walls(self, x_left, x_right, y_top, y_bottom):
		tile_left = (x_left - 1) >> 4
		tile_right = (x_right + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		platforms = []
		
		for tile_x in range(tile_left, tile_right + 1):
			for tile_y in range(tile_top, tile_bottom + 1):
				platforms += self.level_info.get_tile(tile_x, tile_y).get_platforms()['solid']
				
		return platforms
	
	def get_landing_surfaces(self, x, y_top, y_bottom):
		tile_left = (x - 1) >> 4
		tile_right = (x + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		return self.level_info.get_landing_platforms_in_rectangle(tile_left - 1, tile_right + 1, tile_top, tile_bottom)
	
	def get_ceilings(self, x, y_top, y_bottom):
	
		tile_left = (x - 1) >> 4
		tile_right = (x + 1) >> 4
		tile_top = (y_top - 1) >> 4
		tile_bottom = (y_bottom + 1) >> 4
		
		return self.level_info.get_ceilings_in_rectangle(tile_left, tile_right, tile_top, tile_bottom)
	
	def get_just_inclines(self, x_left, x_right, y_top, y_bottom):
	
		tile_left = (x_left >> 4) - 1
		tile_right = (x_right >> 4) + 1
		tile_top = (y_top >> 4) - 1
		tile_bottom = (y_bottom >> 4) + 1
		
		return self.level_info.get_inclines_in_rectangle(tile_left, tile_right, tile_top, tile_bottom)
	
	def IsPlatformOn(self, pixel_x, pixel_y):
		x = int(pixel_x / 16)
		y = int(pixel_y / 16)
		return len(self.level_info.get_landing_platforms_in_rectangle(x, x, y, y)) > 0
	
	def ProcessInput(self, events):
		
		x = int(self.player.x / 16)
		y = int(self.player.y / 16)
		current_tile = self.level_info.get_tile(x, y)
		below_tile = self.level_info.get_tile(x, y + 1)
		above_tile = self.level_info.get_tile(x, y - 1)
		
		in_water = current_tile.is_water()
		on_ladder = current_tile.is_ladder()
		ladder_above = above_tile.is_ladder()
		ladder_below = below_tile.is_ladder()
		on_death_tile = current_tile.is_kill()
		on_ouch_tile = current_tile.is_ouch()
		
		for event in events:
			if event.key == 'start' and event.down:
				self.next = TransitionScene(self, PauseScene(self), 'fade', 10)
				jukebox.MakeQuiet()
			elif event.key == 'B':
				# jump
				if event.down and (self.player.on_ground or in_water or self.player.holding_ladder):
					if in_water:
						self.player.vy = -4
					else:
						self.player.vy = -15
					self.player.holding_ladder = False
					self.player.on_ground = False
					self.player.platform = None
				elif self.player.vy < 0:
					self.player.vy = 0
			elif event.key == 'Y' and event.down:
				if self.wand_cooldown <= 0 and len(self.bullets) < 5 and wandStatus.DepleteMagic():
					self.wand_cooldown = 5
					self.bullets.append(Bullet(self.player.left_facing, self.player.x, self.player.y, wandStatus.SelectedWand()))
			elif event.key == 'Y' and event.up and self.wand_charge > 10:
				if wandStatus.SelectedWand() == 4:
					charge = max(0, min(2, int((self.wand_charge - 10) / 30.0)))
					self.bullets.append(Bullet(self.player.left_facing, self.player.x, self.player.y, wandStatus.SelectedWand(), charge))
					self.wand_charge = 0
			elif event.key == 'L' and event.up: #TODO: remove this before shipping
				self.level_info.Refresh()
		
		running = input.is_key_pressed('A') and (not in_water)
		
		if input.is_key_pressed('Y'):
			self.wand_charge += 1
		else:
			self.wand_charge = 0
		
		if input.is_key_pressed('left'):
			self.player.left_facing = True
			self.target_vx = (-3, -5)[running]
		elif input.is_key_pressed('right'):
			self.player.left_facing = False
			self.target_vx = (3, 5)[running]
		else:
			self.target_vx = 0
		
		if in_water:
			if self.player.on_ground:
				self.target_vx /= 3.0
			else:
				self.target_vx /= 1.3
		
		if self.wand_cooldown > 0:
			self.target_vx = 0
		
		screechiness = 0.6 #TODO: make this dynamic for low-friction ice levels
		if self.target_vx != self.player.vx:
			if self.target_vx > self.player.vx:
				self.player.vx = min(self.target_vx, self.player.vx + screechiness)
			elif self.target_vx < self.player.vx:
				self.player.vx = max(self.target_vx, self.player.vx - screechiness)
	
	def Update(self):
		self.counter += 1
		
		self.wand_cooldown -= 1
		
		if self.counter == 1:
			#print 'attempting to play: ', self.level_info.level_template.values['music']
			jukebox.PlayLevelMusic(self.level_info.level_template.values['music'])
		
		camera = self.get_camera_offset()
		camera_x = camera[0]
		camera_y = camera[1]
		
		new_bullets = []
		for bullet in self.bullets:
			bullet.update()
			if bullet.is_off_screen(camera_x, camera_x + 256):
				bullet.void_this()
			
			if not bullet.expired:
				new_bullets.append(bullet)
		self.bullets = new_bullets
		
		if self.allow_enemy_edit:
			if _enemyEdit.ModeToggled():
				self.enemy_edit_mode = not self.enemy_edit_mode
				if not self.enemy_edit_mode:
					
					filename = 'levels' + os.sep + 'levels' + os.sep + self.level_id + self.screen_id + '.txt'
					c = open(filename, 'rt')
					lines = trim(c.read()).split('\n')
					output = ''
					for line in lines:
						parts = line.split(':')
						if not parts[0] == 'enemies':
							output += line + '\r\n'
					
					enemies = []
					for enemy in self.level_info.level_template.values['enemies']:
						enemies.append(enemy[0] + ',' + str(enemy[1]) + ',' + str(enemy[2]))
					if len(enemies) > 0:
						output += 'enemies:' + ' '.join(enemies) + '\r\n'
					c = open(filename, 'wt')
					c.write(trim(output))
					c.close()
					
					
			
			if self.enemy_edit_mode:
				num = _enemyEdit.NumPressed()
				if num >= 0:
					insert = None
					if num == 1:
						insert = 'bat'
					elif num == 2:
						insert = 'skeleton'
					elif num == 3:
						insert = 'burrower'
					elif num == 4:
						insert = 'greenblob'
					elif num == 5:
						insert = 'blueblob'
					elif num == 6:
						insert = 'redblob'
					elif num == 7:
						insert = 'jellyfish'
					elif num == 8:
						insert = 'orc'
					elif num == 10:
						insert = 'earththingy'
					elif num == 11:
						insert = 'frostthingy'
					elif num == 12:
						insert = 'flarethingy'
					if insert != None:
						self.level_info.level_template.values['enemies'].append((insert, int(self.player.x / 16), int(self.player.y / 16) + 1))
						self.enemies = self.level_info.get_enemies()
					
		
		for sprite in self.get_sprites():
			
			if sprite != self.player:
				if sprite.get_right() < camera_x - 48:
					continue
				if sprite.get_left() > camera_x + 256 + 48:
					continue
				if sprite.get_bottom() < camera_y - 48:
					continue
				if sprite.get_top() > camera_y + 224 + 48:
					continue
			
			x = int(sprite.x / 16.0)
			y = int(sprite.y / 16.0)
			
			current_tile = self.level_info.get_tile(x, y)
			in_water = current_tile.is_water()
			on_ladder = (self.player == sprite) and current_tile.is_ladder()
			ladder_above = (self.player == sprite) and self.level_info.get_tile(x, y - 1).is_ladder()
			ladder_below = (self.player == sprite) and self.level_info.get_tile(x, y + 1).is_ladder()
			residually_on_ladder = self.level_info.get_tile(x, int(sprite.get_bottom() / 16.0)).is_ladder()
			on_death_tile = current_tile.is_kill()
			on_ouch_tile = current_tile.is_ouch()
			
			if sprite == self.player:
				self.player.holding_ladder = self.player.holding_ladder and (ladder_above or on_ladder or residually_on_ladder)
				
			sprite.update(self)
			
			if self.player.special_state != None and self.player.special_state.block_update:
				continue
			
			sprite.dx = sprite.vx
			new_x = int(sprite.x + sprite.dx)
			
			sprite.walked_into_wall = False
			
			if sprite.confined_to_scene:
				new_x = max(2, min(self.level_info.get_width() * 16 - 2, new_x))
			
			if not sprite.moves_through_walls:
				
				if sprite.dx > 0: #going right
					wall = self.find_leftmost_wall_in_path(sprite.x, new_x, sprite.get_head_bonk_top(), sprite.get_bottom())
					if wall != None:
						new_x = wall.get_left_wall_x() - 1
						sprite.vx = 0
						sprite.walked_into_wall = True
				elif sprite.dx < 0: #going left
					wall = self.find_rightmost_wall_in_path(new_x, sprite.x, sprite.get_head_bonk_top(), sprite.get_bottom())
					if wall != None:
						sprite.vx = 0
						new_x = wall.get_right_wall_x() + 1
						sprite.walked_into_wall = True
			
			# player may have possibly jumped through an incline
			if not sprite.on_ground and new_x != sprite.x:
				
				inclines = []
				
				sprite_bottom = sprite.get_bottom()
				
				for incline in self.get_just_inclines(min(new_x, sprite.x) - 2, max(new_x, sprite.x) + 2, sprite.y - 1, sprite.y + 1):
					
					#we're only interested in inclines in the horizontal component
					top = min(incline.y_left, incline.y_right)
					bottom = max(incline.y_left, incline.y_right)
					if sprite_bottom >= top and sprite_bottom <= bottom:
						#if new_x > sprite.x and incline.y_left > incline.y_right:
							inclines.append(incline)
						#elif new_x < sprite.x and incline.y_left < incline.y_right:
						#	inclines.append(incline)
				
				for incline in inclines:
				
					starts_above = sprite_bottom < incline.get_y_at_x(sprite.x)
					ends_above = sprite_bottom < incline.get_y_at_x(new_x)
					
					if starts_above and not ends_above:
						sprite.x = incline.get_x_at_y(sprite.y)
						
						#if incline.is_x_in_range(new_x):
						sprite.platform = incline
						sprite.on_ground = True
						sprite.vy = 0
						self.set_sprite_on_platform(sprite, incline)
						break
			
			sprite.x = new_x
			
			
			if not sprite.on_ground and not sprite.immune_to_gravity:
				if sprite == self.player and self.player.holding_ladder:
					g = 0
				elif in_water:
					g = self.water_g
				else:
					g = self.g
				sprite.vy += g
				
				sprite.vy = min(sprite.vy, 13)
			else:
				sprite.vy = 0
				
			sprite.dy = int(sprite.vy)
			
			if sprite == self.player:
			
				sprite.ladder_climb = input.is_key_pressed('up') or input.is_key_pressed('down')
				
				if self.player.holding_ladder:
					if input.is_key_pressed('up'):
						sprite.dy -= 1
					elif input.is_key_pressed('down'):
						sprite.dy += 1
				else:
					if ladder_below and input.is_key_pressed('down'):
						sprite.y += 4
						sprite.on_ground = False
						sprite.platform = None
						sprite.holding_ladder = True
						sprite.vx = 0
						sprite.dx = 0
						sprite.vy = 0
					elif on_ladder and input.is_key_pressed('up'):
						
						sprite.vx = 0
						sprite.vy = 0
						sprite.dx = 0
						self.player.holding_ladder = True
						sprite.platform = None
						sprite.on_ground = False
						sprite.dy = -1
						
			
			new_y = sprite.y + sprite.dy
			
			if sprite.dy > 0:
				# sprite is falling
				
				y_offset = sprite.get_bottom() - sprite.y
				
				highest = self.find_highest_platform_in_path(sprite.x, sprite.y + y_offset, new_y + y_offset)
				
				if highest != None:
					sprite.on_ground = True
					sprite.platform = highest
					self.set_sprite_on_platform(sprite, highest)
				else:
					sprite.y = new_y
			elif sprite.dy <= 0 and sprite.platform == None:
				
				y_offset = sprite.get_head_bonk_top() - sprite.y
				
				lowest = self.find_lowest_platform_in_path(sprite.x, new_y + y_offset, sprite.y + y_offset)
				
				if lowest != None:
					sprite.dy = 0
					sprite.vy = 0
					new_y = lowest.get_bottom() + y_offset
					#TODO: play BONK noise
					
				else:
					sprite.y = new_y
			
			else:
				if sprite.platform != None:
					platform = sprite.platform
					if platform.is_x_in_range(sprite.x):
						self.set_sprite_on_platform(sprite, platform)
					else:
						# player walked off edge of platform
						
						new_platform_found = False
						
						# which way?
						if sprite.x < platform.left:
							# walked off left
							left = platform.left
							for left_platform in self.get_landing_surfaces(left - 1, sprite.y - 18, sprite.y + 18):
								
								# check to see if the right side of this platform is vertically aligned with 
								# the left side of the one you walked off
								if abs(left_platform.left + left_platform.width - platform.left) <= 1:
									
									# check to see if they're vertically aligned
									if abs(left_platform.y_right - platform.y_left) <= 1:
										sprite.platform = left_platform
										break
	
						else:
							# walked off right
							right = platform.left + platform.width
							for right_platform in self.get_landing_surfaces(right + 1, sprite.y - 18, sprite.y + 18):
								
								# check to see if the left side of this platform is vertically aligned with 
								# the right side of the one you walked off
								if abs(right_platform.left - (platform.left + platform.width)) <= 1:
									
									# check to see if they're vertically aligned
									if abs(right_platform.y_left - platform.y_right) <= 1:
										sprite.platform = right_platform
										break
						
						# if no new platform was found...
						if sprite.platform == platform:
							#the sprite has fallen off the edge
							sprite.on_ground = False
							sprite.platform = None
			
			if sprite != self.player:
				if sprite.is_powerup:
					pass
				elif not sprite.invincible:
					for bullet in self.bullets:
						if sprite.is_collision_with_rect(bullet.x - 6, bullet.x + 6, bullet.y - 4, bullet.y + 4):
							bullet.void_this()
							sprite.killed = sprite.hit(bullet.get_additional_damage())
		
		
		
		new_sprites = []
		
		for powerup in self.powerups:
			if powerup.is_collision_with_rect(self.player.get_left(), self.player.get_right(), self.player.get_top(), self.player.get_bottom()):
				powerup.collected(self)
			else:
				new_sprites.append(powerup)
		self.powerups = new_sprites
		
		new_sprites = []
		
		for enemy in self.enemies:
			if not enemy.killed:
				new_sprites.append(enemy)
			else:
				powerup = enemy.GetPowerUp(self.counter, self)
				self.other_sprites.append(PoofCloud(enemy.x, enemy.y))
				if powerup != None:
					self.powerups.append(powerup)
		self.enemies = new_sprites
		
		new_sprites = []
		
		for foo in self.other_sprites:
			if not foo.expired:
				new_sprites.append(foo)
		self.other_sprites = new_sprites
		
		if self.mumblefoo != None and self.mumblefoo.lifetime > 6:
			if self.is_collision(self.mumblefoo, self.player):
			
				self.wibblywobbly_counter = min(self.wibblywobbly_counter, self.wibblywobbly.get_max_severity())
				self.mumblefoo = None
				# TODO: play noise
				jukebox.MumblefooPickedUp()
				if self.text_triggers['soul_pickup'] != None:
					self.text_triggers['timer'].append((self.counter + 40, self.text_triggers['soul_pickup'][0], self.text_triggers['soul_pickup'][1]))
		
		if not self.enemy_edit_mode:
			if self.player.flashing_counter <= 0:
				for sprite in self.enemies:
					if self.is_collision(sprite, self.player):
						if self.mumblefoo == None:
							# You dropped the mumblefoo!
							jukebox.MumblefooDropped()
							self.mumblefoo = SoulJar(self.player.x, self.player.y, self.counter)
						self.vy = -4
						self.player.flashing_counter = 60
						if self.player.left_facing:
							self.vx = 5
						else:
							self.vx = -5
		
		if self.mumblefoo == None:
			self.wibblywobbly_counter = max(0, self.wibblywobbly_counter - 5)
			
			# Check for door entry
			door = self.level_info.get_door_dest(int(self.player.x / 16), int(self.player.y / 16))
			if door != None and self.player.special_state == None:
				self.player.special_state = SpecialStateDoorEntry(door, self.player)
			
			# Check for victory
			victory_x = self.level_info.get_victory_x()
			if victory_x > 0 and self.player.x >= victory_x and self.player.special_state == None:
				#TODO: automated victory sequence
				games.active_game().save_value('finished_world' + self.level_id, 1)
				parts = self.level_id.split('_')
				world = int(parts[0])
				level_from = int(parts[1][0])
				level_to = str(level_from + 1)
				level_from = str(level_from)
				if level_to == '6':
					level_to = 'next'
				if world == 0:
					level_from = '1'
					level_to = '1'
					world = 1
				
				jukebox.PlayVictory()
				
				if self.level_id == '3_5':
					nextScene = CutSceneScene('endgame', CreditsScene())
				else:
					nextScene = MapScene(world, level_from, level_to)
				
				self.player.special_state = SpecialStateVictory(self.player, nextScene)
			
		else:
			self.wibblywobbly_counter += 1
			if self.player.special_state == None and self.wibblywobbly_counter > self.wibblywobbly.get_max_severity():
				if self.level_id != '0_1':
					self.kill_player()
		
		if self.player.special_state == None and self.player.y > self.level_info.get_height() * 16 + 30:
			self.kill_player()
		
		new_text_triggers = []
		for text_trigger in self.text_triggers['timer']:
			if self.counter >= text_trigger[0] and self.next == self:
				self.next = TextOverlayScene(text_trigger[1], self, text_trigger[2])
			else:
				new_text_triggers.append(text_trigger)
		self.text_triggers['timer'] = new_text_triggers
		
	def get_left_stiched_platform(self, platform):
		for stiched in self.get_landing_surfaces(platform.left - 1, platform.y_left - 3, platform.y_left + 3):
			if abs(platform.y_left - stiched.y_right) <= 1 and abs(platform.left - stiched.left - stiched.width) <= 1:
				return stiched
		return None
	
		
	def get_right_stiched_platform(self, platform):
		for stiched in self.get_landing_surfaces(platform.left + platform.width + 1, platform.y_right - 3, platform.y_right + 3):
			if abs(platform.y_right - stiched.y_left) <= 1 and abs(platform.left + platform.width - stiched.left) <= 1:
				return stiched
		return None
	
	def kill_player(self):
		self.player.special_state = SpecialStateDying(self.player)
		jukebox.PlayDeath()
	
	def is_collision(self, spriteA, spriteB):
		
		return spriteA.is_collision_with_rect(
			spriteB.get_left(),
			spriteB.get_right(),
			spriteB.get_top(),
			spriteB.get_bottom())
	
	def set_sprite_on_platform(self, sprite, platform):
		sprite.y = int(platform.get_y_at_x(sprite.x) - sprite.height + sprite.height / 2) # odd math to keep consistent rounding
	
	def find_leftmost_wall_in_path(self, left_x, right_x, y_top, y_bottom):
		return self._find_first_wall_in_path(left_x, right_x, y_top, y_bottom, True)
	
	def find_rightmost_wall_in_path(self, left_x, right_x, y_top, y_bottom):
		return self._find_first_wall_in_path(left_x, right_x, y_top, y_bottom, False)
	
	
	def _find_first_wall_in_path(self, left_x, right_x, y_top, y_bottom, going_right):
		furthest = None
		
		platforms = self.get_walls(left_x, right_x, y_top, y_bottom)
		
		for platform in platforms: # all platforms are guaranteed to be solid type
			if not (y_bottom <= platform.get_top() or y_top > platform.get_bottom()):
				if going_right:
					wall_x = platform.left
				else:
					wall_x = platform.left + platform.width
					
				if left_x <= wall_x and right_x >= wall_x:
					if furthest == None:
						furthest = platform
					elif going_right and furthest.left > platform.left:
						furthest = platform
					elif not going_right and furthest.left + furthest.width < platform.left + platform.width:
						furthest = platform
		return furthest
		
	def _find_first_platform_in_path(self, x, upper_y, lower_y, going_down):
		furthest = None
		
		if going_down:
			platforms = self.get_landing_surfaces(x, upper_y, lower_y)
		else:
			platforms = self.get_ceilings(x, upper_y, lower_y)
		
		for platform in platforms:
			if platform.is_x_in_range(x):
				if going_down:
					platform_y = platform.get_y_at_x(x)
				else:
					platform_y = platform.get_bottom()
					
				if upper_y <= platform_y and lower_y >= platform_y:
					if furthest == None:
						furthest = platform
					elif going_down and furthest.get_y_at_x(x) > platform_y:
						furthest = platform
					elif not going_down and furthest.get_bottom() < platform.get_bottom():
						furthest = platform
		
		return furthest
		
	def find_highest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, True)

	def find_lowest_platform_in_path(self, x, upper_y, lower_y):
		return self._find_first_platform_in_path(x, upper_y, lower_y, False)
		
	def Render(self, screen):
		
		self.render_counter += 1
		
		self.update_camera()
		camera = self.get_camera_offset()
		cx = camera[0]
		cy = camera[1]
		
		bg = self.level_info.get_background_image(self.counter)
		if bg != None:
			scroll_width = (self.level_info.get_width() * 16 - 256)
			if scroll_width == 0: scroll_width = 1
			bg_percent = (0.0 + cx) / scroll_width
			bg_width = bg.get_width()
			
			bg_offset = -1 * bg_percent * (bg_width - 256)
			
			bg_offset += self.level_info.get_background_offset(self.render_counter)
			
			bg_offset = int(bg_offset % bg.get_width())
			screen.blit(bg, (bg_offset, 0))
			screen.blit(bg, (bg_offset - bg.get_width(), 0))
		
		col_start = max(0, int(cx / 16 - 1))
		col_end = min(self.level_info.get_width() - 1, col_start + 18)
		
		row_start = max(0, int(cy / 16 - 1))
		row_end = min(self.level_info.get_height() - 1, row_start + 16)
		
		for row in range(row_start, row_end + 1):
			for col in range(col_start, col_end + 1):
				x = col * 16
				y = row * 16
				tile = self.level_info.get_tile(col, row)
				imgs = tile.get_images(self.render_counter)
				if imgs != None:
					for img in imgs:
						if img != None:
							screen.blit(img, (x - cx, y - cy))
		
		if self.wibblywobbly_counter > 0:
			self.wibblywobbly.render_color_fade(screen, self.render_counter, self.wibblywobbly_counter)
		
		self.player.wand_cooldown= self.wand_cooldown
		
		for sprite in self.get_sprites():
			sprite.draw(screen, self.player.vx != 0, self.counter, camera)
		
		for bullet in self.bullets:
			bullet.draw(screen, cx, cy)
		
		if self.wibblywobbly_counter > 0:
			self.wibblywobbly.render(screen, self.render_counter, self.wibblywobbly_counter)

		self.render_status(screen)
		
		if self.enemy_edit_mode:
			label = get_text("(enemy insertion mode)")
			screen.blit(label, (0, 0))
	
	def render_status(self, screen):
		if self.renderInventory:
			left = 256 - 10 - 100
			top = 5
			pygame.draw.rect(screen, (0, 0, 0), Rect(left - 1, top - 1, 102, 8))
			wand_width = wandStatus.GetMagic()
			colors = wandStatus.GetColors()
			pygame.draw.rect(screen, colors[0], Rect(left, top, wand_width, 5))
			pygame.draw.rect(screen, colors[1], Rect(left, top + 2, wand_width, 3))
			pygame.draw.rect(screen, colors[2], Rect(left, top + 4, wand_width, 2))
		
		
			

class EnemyEditInput:
	def __init__(self):
		self.num_pressed = -1
		self.toggle_mode = False
	
	def Clear(self):
		self.num_pressed = -1
		self.toggle_mode = False
		
	
	def Update(self, event):
		if event.type == KEYUP:
			if event.key == K_0:
				self.num_pressed = 10
			elif event.key == K_p:
				self.num_pressed = 11
			elif event.key == K_EQUALS:
				self.num_pressed = 12
			elif event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0):
				self.num_pressed = event.key - K_0
			if event.key == K_e:
				self.toggle_mode = True
	def ModeToggled(self):
		return self.toggle_mode
	def NumPressed(self):
		return self.num_pressed
		
#STATIC
_enemyEdit = EnemyEditInput()