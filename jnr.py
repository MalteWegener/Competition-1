import pygame,utils,Col2D

pygame.init()
screen = pygame.display.set_mode((500,500))

player = utils.Player((0,200), (0,255,0))
objects = [utils.Rectangle((0,450),(500,50),(255,255,0)),utils.Rectangle((0,300),(500,5),(255,255,0))]
lasttick = 0
while True:
	curtick = pygame.time.get_ticks()
	dt = (curtick-lasttick)/1000

	screen.fill((0,0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			player.jump(objects)

	player.update(dt,objects)

	player.draw(screen)
	for obj in objects:
		obj.draw(screen)


	lasttick = curtick
	pygame.display.flip()