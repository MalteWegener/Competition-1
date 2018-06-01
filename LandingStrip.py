import numpy as np
from pygame import gfxdraw
from math import *
import matplotlib.pyplot as plt
import sys
import pygame

class light():
	def __init__(self, x,y,z,col):
		#Transform from idiot coordinate to homogeneous coordinates in OpenGL Standard
		self.pos = np.array([y,z,-x,1])
		self.col = col

class Camera():
	def __init__(self,x,y,z,fov,near,far,pitch, yaw, roll):
		self.matTrans = np.identity(4)
		self.matTrans[0,3]=x
		self.matTrans[1,3]=y
		self.matTrans[2,3]=z

		self.Proj = np.zeros([4,4])
		self.Proj[0,0] = 1/tan(radians(fov)/2)
		self.Proj[1,1] = 1/tan(radians(fov)/2)
		self.Proj[2,2] = -(far+near)/(far-near)
		self.Proj[2,3] = -2*(far+near)/(far-near)
		self.Proj[3,2] = -1

		Rot1 = np.zeros([4,4]) 
		Rot1[0,0] = 1
		Rot1[3,3] = 1
		Rot1[1,1] = cos(radians(pitch))
		Rot1[2,2] = cos(radians(pitch))
		Rot1[1,2] = -sin(radians(pitch))
		Rot1[2,1] = sin(radians(pitch))

		Rot2 = np.zeros([4,4]) 
		Rot2[0,0] = cos(radians(yaw))
		Rot2[3,3] = 1
		Rot2[0,2] = sin(radians(yaw))
		Rot2[2,0] = -sin(radians(yaw))
		Rot2[2,2] = cos(radians(yaw))
		Rot2[1,1] = 1

		Rot3 = np.zeros([4,4]) 
		Rot3[2,2] = 1
		Rot3[3,3] = 1
		Rot3[0,0] = cos(radians(roll))
		Rot3[0,1] = -sin(radians(roll))
		Rot3[1,0] = sin(radians(roll))
		Rot3[1,1] = cos(radians(roll))

		self.Rot = Rot3.dot(Rot1).dot(Rot2)

	def applyonlight(self, light):
		tmp = np.dot(self.matTrans,light.pos)
		tmp = np.dot(self.Rot,tmp)
		tmp2 =np.dot(self.Proj,tmp)
		tmp2 = tmp2/tmp2[3]
		return tmp2, tmp

	def applyonpoint(self,point):
		tmp = np.dot(self.matTrans,point)
		tmp = np.dot(self.Rot,tmp)
		tmp2 =np.dot(self.Proj,tmp)
		tmp2 = tmp2/tmp2[3]
		return tmp2, tmp

	def getunit(self):
		tmp = np.array([0,0,-1,0]).dot(self.Rot)[:3]
		return tmp/np.linalg.norm(tmp)



lines = open("runway_lights-1.dat").readlines()

lightsworldspace =[]

for l in lines:
	if l is not lines[0]:
		tmp = l.replace("\n","").split(",")
		lightsworldspace.append(light(float(tmp[1]),float(tmp[0]),0,(float(tmp[2]),float(tmp[3]),float(tmp[4]))))

for l in lines:
	if l is not lines[0]:
		tmp = l.replace("\n","").split(",")
		lightsworldspace.append(light(float(tmp[1]),float(tmp[0])+100,0,(float(tmp[2]),float(tmp[3]),float(tmp[4]))))

width = height = 800
pygame.init()
screen = pygame.display.set_mode((width,height))

cpos = np.array([0.,50.,0.])
crot = np.array([0.,180.,0.])
myfont = pygame.font.SysFont("monospace", 30)

lastt = 0
while True:
	curt = pygame.time.get_ticks()
	Cam = Camera(cpos[0],cpos[1],cpos[2],90,0.01,5,crot[0],crot[1],crot[2])
	screen.fill((0,0,0))
	for l in lightsworldspace:
		tmp, tmp2 = Cam.applyonlight(l)
		x = 1 + tmp[0]
		y = 1 - tmp[1]
		x *= width/2
		y *= height/2
		if tmp2[2] > 0 and (0<=x<=width and 0<= y <= height):
			pygame.draw.circle(screen,l.col,(int(x),int(y)),1)
	#Leave this in otherwise it crashes like your grades

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		crot[0] -= 1
	if keys[pygame.K_s]:
		crot[0] += 1

	if keys[pygame.K_d]:
		crot[1] += 1
	if keys[pygame.K_a]:
		crot[1] -= 1

	if keys[pygame.K_q]:
		crot[2] += 1
	if keys[pygame.K_e]:
		crot[2] -= 1

	if keys[pygame.K_SPACE]:
		print(Cam.getunit())
		cpos += Cam.getunit()

	pygame.display.update()
