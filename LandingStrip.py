import numpy as np
from pygame import gfxdraw
from math import *
import matplotlib.pyplot as plt
import sys
import pygame

lines = open("runway_lights-1.dat").readlines()

class light():
	def __init__(self, x,y,col):
		#Transform from idiot coordinate to homogeneous coordinates in OpenGL Standard
		self.pos = np.array([y,0,-x,1])
		self.col = col

class Camera():
	def __init__(self,x,y,z,fov,near,far,pitch):
		self.matTrans = np.identity(4)
		self.matTrans[0,3]=x
		self.matTrans[1,3]=y
		self.matTrans[2,3]=z

		self.Proj = np.zeros([4,4])
		self.Proj[0,0] = 1/tan(radians(fov)/2)
		self.Proj[1,1] = 1/tan(radians(fov)/2)
		self.Proj[2,2] = -(far+near)/(far-near)
		self.Proj[3,3] = -2*(far+near)/(far-near)
		self.Proj[3,2] = -1

		self.Rot = np.zeros([4,4]) 
		self.Rot[0,0] = 1
		self.Rot[3,3] = 1
		self.Rot[1,1] = cos(radians(pitch))
		self.Rot[2,2] = cos(radians(pitch))
		self.Rot[1,2] = -sin(radians(pitch))
		self.Rot[2,1] = sin(radians(pitch))

	def apply(self, light):
		tmp = np.dot(self.matTrans,light.pos)
		tmp = np.dot(self.Rot,tmp)
		tmp =np.dot(self.Proj,tmp)
		tmp = tmp/tmp[3]
		return tmp

lightsworldspace =[]

x =[]
y=[]

for l in lines:
	if l is not lines[0]:
		tmp = l.replace("\n","").split(",")
		lightsworldspace.append(light(float(tmp[1]),float(tmp[0]),(float(tmp[2]),float(tmp[3]),float(tmp[4]))))

		x.append(float(tmp[1]))
		y.append(float(tmp[0]))

width = height = 500
pygame.init()
screen = pygame.display.set_mode((width,height))

cz = -300
cx = 0
cy = 50
cp = 0
fov = 90
myfont = pygame.font.SysFont("monospace", 30)
while True:
	Cam = Camera(cx,cy,cz,fov,0.01,3000,cp)
	screen.fill((0,0,0))
	for l in lightsworldspace:
		tmp = Cam.apply(l)
		tmp2 = np.dot(Cam.matTrans, l.pos)
		x = 0.5 + tmp[0]
		y = 0.5 + tmp[1]
		x *= width
		y *= height
		if ((tmp[1]<=0 and tmp2[1]<=0) or (tmp[1]>0 and tmp2[1]>0)):
			pygame.draw.circle(screen,l.col,(int(x),int(y)),1)
	#Leave this in otherwise it crashes like your grades
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	if event.type == pygame.MOUSEBUTTONDOWN:
		print("debug")
		if event.button == 1:
			fov += 0.1
		elif event.button == 3:
			fov -= 0.1

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		cz += 0.5
	if keys[pygame.K_s]:
		cz -= 0.5

	if keys[pygame.K_d]:
		cx -= 0.5
	if keys[pygame.K_a]:
		cx += 0.5

	if keys[pygame.K_SPACE]:
		cy += 0.5
	if keys[pygame.K_e]:
		cy -= 0.5

	if keys[pygame.K_UP]:
		cp += 0.3
	if keys[pygame.K_DOWN]:
		cp -= 0.3

	screen.blit(myfont.render("FOV: " + str(fov)[:5], 1, (255,255,0)), (50, 50))
	pygame.display.update()