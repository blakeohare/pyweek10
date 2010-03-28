class CutSceneScene:
   def __init__(self):
      self.next = self
      self.counter = 0

   def ProcessInput(self, events):
      pass
   
   def Render(self, screen):
      # the screen will be 256x244 pixels
      pass
   
   def Update(self):
      self.counter += 1