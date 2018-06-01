import GL
import numpy as np
import pygame
import sys

class Camera:
	def __init__(self, pos, rot,width,heigh):
		self.Trans = GL.TranslateNeg(pos)
		self.Rot =GL.Rot(rot)
		self.Proj = GL.Projection(width/height,100,0.1,300)

	def apply(self,pt):
		tmp = np.dot(self.Trans,pt)
		tmp = np.dot(self.Rot,tmp)
		tmp2 = np.dot(self.Proj,tmp)
		tmp2 = tmp2/tmp2[3]
		return tmp2,tmp

	def getunit(self):
		return (-1*self.Rot).dot([0.,0.,1.,0.])

class Runway:
	def __init__(self):
		raw = np.genfromtxt("runway_lights-1.dat",delimiter=",",comments="#")
		self.pos = []
		self.colour = []
		for i in range(raw.shape[0]):
			#homogeneous Coordinates
			self.pos.append(np.array([raw[i,0],0.,-raw[i,1],1]))
			self.colour.append((raw[i,2],raw[i,3],raw[i,4]))

	def render(self, screen, width, height, cam):
		for i in range(len(self.pos)):
			p,p2 = cam.apply(self.pos[i])
			x = (0.5+p[0])*width
			y = (0.5-p[1])*height
			if p2[2]<0 and 0<=x<=width and 0<=y<=height:
				pygame.draw.circle(screen, self.colour[i],(int(x),int(y)),1)


#main Prog
width = 400
height = 400

cpos = np.array([0,60,100])
crot = np.array([0,0,0])

rw = Runway()

pygame.init()
screen = pygame.display.set_mode((width,height))

while True:
	cam = Camera(cpos,crot,width,height)
	print(cam.getunit()[:3])
	cpos = cpos + cam.getunit()[:3]
	screen.fill((0,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		crot[0] += 1
	if keys[pygame.K_s]:
		crot[0] -= 1

	if keys[pygame.K_a]:
		crot[1] -= 1
	if keys[pygame.K_d]:
		crot[1] += 1

	if keys[pygame.K_q]:
		crot[2] -= 1
	if keys[pygame.K_e]:
		crot[2] += 1

	rw.render(screen,width,height,cam)
	pygame.display.update()
