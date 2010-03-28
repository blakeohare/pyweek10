
pygame.init()

screen = pygame.display.set_mode((800, 600))

counter = 0

done = False

while not done:
	
	start = time.time()
	
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			done = True
	
	screen.fill((0,0,0))
	
	x = int(counter % 800)
	y = int(counter % 600)
	
	pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)
	
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