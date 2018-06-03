import pygame
import numpy as np
from math import *
import GL
import sys
from rotationmodel import Airplane

#This class provides an abstraction for the game scene
#maybe writing it like dis makes it a lot more abstract
#but it will make extending the game way easier
# Rule No.0: You dont write code, you write solutions
class Scene:
	def __init__(self):
		self.objects = []

	def render(self, screen, cam, width, height):
		for o in self.objects:
			o.render(screen, cam, width, height)

#That camera aint a snitch, because it can look away
class Camera:
	#position and rotation are each a 1x3 array
	def __init__(self,pos,rot,width,height):
		#becuase we have the position and rotation
		#of the cam in the world frame, but we need to
		#transform the world angainst the camera so negative all of it
		self.Translation = GL.TranslateNeg(pos)
		self.Rotation = GL.Rot(-1*rot)
		self.Projection = GL.Projection(width/height,60,0.01,3000)

	def apply(self, position):
		relpos = np.dot(self.Translation,position)
		relpos = np.dot(self.Rotation,relpos)
		renderpos =np.dot(self.Projection,relpos)
		return relpos, renderpos

	def getunit(self):
		return self.Rotation.dot(np.array([0,0,-1,0]))[:3]

#This provides a base for all renderable objects
#Real Object Oriented Languages, would have the pussybility
#to make this class virtual, and the class abstract.
#So this class cant be build, but if something inherits from
#it has all functionality
class GameObject:

	#the off and rot are transformation matrixes from the origin
	def __init__(self, off, rot):
		IsThisRealOOP = "No"

	#basic render function
	#Actually it does nothing, as you hopefully see
	#Thats why virtual functions exist
	def render(self, screen, cam, width, height):
		pythonsucks = True


#A light is nice and thats why it shoulf be its own
#object. COuld be a struct, but hey its python
class light:
	def __init__(self, pos, colour):
		self.pos = pos
		self.colour = colour

#Lets make a runway nigga
#it makes no blinky blinky, but we can add it
class Runway(GameObject):
	def __init__(self, off, rot):
		raw = np.genfromtxt("runway_lights-1.dat",delimiter=",",comments="#")
		#This is pretty self don't you think
		self.lights = []

		#we make a list of all the lights
		for i in range(raw.shape[0]):
			#we first convert to homogeneous coordinates and then apply
			#the Transformation matrixes
			#second argument is the colour as an rgb tuple
			self.lights.append(light(off.dot(rot).dot(np.array([raw[i,0],0.,-raw[i,1],1])),(raw[i,2],raw[i,3],raw[i,4])))

	#dis where we overwrite the useless function from the game object
	def render(self, screen, cam, width, height):
		#just go through all the lights, apply the cam and
		#then dont render it if its behind the cam
		#nothing that lays behind you should matter to you
		for l in self.lights:
			#to be honest: this is like the worst time efficiency in the code
			relpos, renderpos = cam.apply(l.pos)
			#Like at the moment the render position is not homogeneous
			#so we make it homogeneous, but only if its not to close to 0
			if relpos[2]<0 and not(-0.001<renderpos[3]<0.001):
				#make the coordinate homogeneous
				renderpos = renderpos/renderpos[3]
				#then we make it to x,y space and invert y because python is a
				#special child
				x = (1+renderpos[0])*width/2
				y = (1-renderpos[1])*height/2
				# now we cutoff if its outside the screen, because that saves time
				if 0<=x<=width and 0<=y<=height:
					pygame.draw.circle(screen,l.colour,(int(x),int(y)),1)

class WTC(Runway):
	def __init__(self,offpos,offrot):
		self.lights = []

		#make 100 floors
		for i in range(100):
			positions = [[0,0],[0,5],[0,10],[0,15],[0,20],[5,20],[10,20],[15,20],[20,20],
						[20,15],[20,10],[20,5],[20,0],[15,0],[10,0],[5,0]]

			for p in positions:
				tmppos = np.array([p[0],5*i,p[1],1])
				self.lights.append(light(offpos.dot(offrot).dot(tmppos),(0,255,255)))

#quick mockup nigga
plane = Airplane(np.array([0,50,400]))

width = 800
height = 500

pygame.init()
screen = pygame.display.set_mode((width,height))

scene = Scene()
cam = Camera(plane.pos,plane.rot,width,height)
#if you dont want to have the runway transformed give it 4*4 Identity matrixes
scene.objects.append(Runway(np.identity(4),np.identity(4)))
#scene.objects.append(Runway(GL.Translate([50,0,20]),GL.Roty(-30)))
#scene.objects.append(WTC(GL.Translate([-50,0,0]),np.identity(4)))

while True:
	print(plane.rot)
	plane.pos = plane.pos + 5*cam.getunit()
	cam = Camera(plane.pos,plane.rot,width,height)
	screen.fill((15,15,15))
	scene.render(screen, cam, width, height)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		plane.pitch(2)
	if keys[pygame.K_s]:
		plane.pitch(-2)

	pygame.display.update()
