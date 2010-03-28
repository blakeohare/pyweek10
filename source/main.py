
pygame.init()

screen = pygame.display.set_mode((800, 600))

counter = 0

scene = LoadScene()

while scene != None:
	
	start = time.time()
	
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			scene = None
			
	if scene == None:
		break
	
	scene.Update()
		
	screen.fill((0,0,0))
	
	scene.Render(screen)
	
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