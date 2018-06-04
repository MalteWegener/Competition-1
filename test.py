import pygame, sys
import utils

from pygame.locals import *

pygame.init()
DISPLAY = pygame.display.set_mode((600,600))
bird = utils.Bird()
lasttick = 0
currenttick = pygame.time.get_ticks()
gates = []
gates.append(utils.Gate())
myfont = pygame.font.SysFont("monospace", 30)
myfont = pygame.font.SysFont("monospace", 5)

while True:
	x,y = pygame.mouse.get_pos()
	DISPLAY.fill((0,0,0))
	score = 0

	if (currenttick/1000) >= 2*len(gates):
		gates.append(utils.Gate())

	for gat in gates:
		if gat.collideswithbird(bird.pos) and False:
			pygame.quit()
			sys.exit()
		gat.update(DISPLAY, (currenttick-lasttick)/1000)
		if 300 > (gat.x+30):
			score += 1

	label = myfont.render(str(score), 1, (255,255,0))
	DISPLAY.blit(label, (100, 100))

	rand = False
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN and event.key == K_SPACE:
			rand = True

	bird.update((currenttick-lasttick)/1000,DISPLAY, rand)

	pygame.display.flip()
	print(1/((currenttick-lasttick)/1000))
	lasttick = currenttick
	currenttick = pygame.time.get_ticks()

"""
Like srsly fucking hell. Writing Python is against my Religion.
I like C++ and stuff. Like where your compiler tells you, that you fucked up,
while it compiles. But our Special child python sits in the corner eating glue and screaming:
	"But i want to have no control over what to pass where and what actually gets passed.
	I dont care if i pass by value or by reference. And you wont know either."
And how the hell can that shit langugae call itself object oriented, if it doesnt know the basic concept
of encapsulation. Like python classes are like that wierd uncle, who wants everyone top access his private members.
Like no fucking way this language should be allowed to be called object oriented.
"""