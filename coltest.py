import Col2D
import pygame
import utils
import random
import math
import sys

pygame.init()
DISPLAY = pygame.display.set_mode((900,900))

rect1 = utils.RegularPolygon((200,200),75,(0,255,255),5,math.pi)
rect2 = utils.RegularPolygon((200,200),50,(255,0,255),3,0)

player = utils.RegularPolygon((200,200),50,(255,0,255),3,0)
ground = utils.Rectangle((0,850),(900,50),(255,255,255))

myfont = pygame.font.SysFont("monospace", 30)
locktomouse1 = False
locktomouse2 = False
locktomouse3 = False
offset = [0,0]
coll = "Tech Demo"
while True:
	DISPLAY.fill((0,0,0))
	x,y = pygame.mouse.get_pos()
	if locktomouse1:
		rect1.updatepos((x+offset[0],y+offset[1]))
	if locktomouse2:
		rect2.updatepos((x+offset[0],y+offset[1]))
	if locktomouse3:
		player.updatepos((x+offset[0],y+offset[1]))
	elif not player.shell.checkColl(ground.shell):
		player.updatepos((player.pos[0],player.pos[1]+2))

	rect1.draw(DISPLAY)
	rect2.draw(DISPLAY)

	player.draw(DISPLAY)
	ground.draw(DISPLAY)
	coll = rect1.shell.checkColl(rect2.shell)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and rect1.shell.checkPoint([x,y]) and event.button ==1 and not locktomouse2:
			offset[0] = rect1.pos[0]-x
			offset[1] = rect1.pos[1]-y
			locktomouse1 = not locktomouse1
		elif event.type == pygame.MOUSEBUTTONDOWN and rect2.shell.checkPoint([x,y]) and event.button ==1 and not locktomouse1:
			offset[0] = rect2.pos[0]-x
			offset[1] = rect2.pos[1]-y
			locktomouse2 = not locktomouse2
		elif event.type == pygame.MOUSEBUTTONDOWN and player.shell.checkPoint([x,y]) and event.button ==1 and not locktomouse1:
			offset[0] = player.pos[0]-x
			offset[1] = player.pos[1]-y
			locktomouse3 = not locktomouse3

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				if locktomouse1:
					rect1.updaterot(rect1.delrot + math.pi/32)
				if locktomouse2:
					rect2.updaterot(rect2.delrot + math.pi/32)
				if locktomouse3:
					player.updaterot(player.delrot + math.pi/32)
			elif event.button == 5:
				if locktomouse1:
					rect1.updaterot(rect1.delrot - math.pi/32)
				if locktomouse2:
					rect2.updaterot(rect2.delrot - math.pi/32)
				if locktomouse3:
					player.updaterot(player.delrot - math.pi/32)
		#coll = not player.shell.checkColl(ground.shell)

	DISPLAY.blit(myfont.render(str(coll), 1, (255,255,0)), (50,50))
	pygame.display.flip()