
class WandStatus:
	def __init__(self):
		self.wand_selected = 0
		self.magic_level = 100

	def GetMagic(self):
		return self.magic_level
	
	def DepleteMagic(self):
		if self.magic_level > 0:
			self.magic_level -= 1
			return True
		return False
	
	def GetColors(self):
		if self.wand_selected == 0:
			return ((130, 0, 130), (110, 0, 110), (90, 0, 90))
		if self.wand_selected == 1:
			return ((0, 128, 255), (0, 64, 255), (0, 0, 220))
		if self.wand_selected == 2:
			return ((255, 160, 30), (255, 80, 0), (240, 0, 0))
		if self.wand_selected == 3:
			return ((255, 255, 0), (200, 200, 0), (150, 150, 0))
		return ((0, 200, 0), (0, 150, 0), (0, 110, 0))
	
	def SelectedWand(self):
		return self.wand_selected
	
	def ShiftWand(self, direction):
		started_with = self.wand_selected
		index = started_with
		while index >= 0 and index <= 4:
			if self.SelectWand(index + direction):
				return
			else:
				index += direction
		self.SelectWand(started_with)
	
	def SelectWand(self, wand_index):
		self.wand_selected = max(0, min(4, wand_index))
		return self.IsKnown(self.wand_selected)
		
	def IsKnown(self, wand_index):
		if wand_index == 0:
			return True
		return games.active_game().get_value('finished_world' + str(wand_index) + '_5') == 1
		
#STATIC
wandStatus = WandStatus()