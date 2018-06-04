#You could delete the whole script part and use this file as a library for your 3d game needs
#Theoretically you could add solid shapes too. Bottle neck is probably, the piece of crap colled interpreter
#He is like that autistic child who is slow as fuck and will only use this one special pen
"""Here you see a better language:

############
##					
##					#			#
##					#			#
##				#########	#########
##					#			#
##					#			#
##
############


Also if you no like meme, turn off television now.
Parental Advisory is reccomended after this Point
"""

import pygame
import numpy as np
from math import *
import GL
import sys
from flightmodel import BetterAirplane

#This class provides an abstraction for the game scene
#maybe writing it like dis makes it a lot more abstract
#but it will make extending the game way easier
class Scene:
	def __init__(self):
		self.objects = []

	#isnt this beatiful overcomplication
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
		self.angles = rot
		self.Translation = GL.TranslateNeg(pos)
		self.Rotation = GL.CamRot(-1*rot)
		self.Projection = GL.Projection(width/height,60,0.1,3000)

		#This just applys the transformation and projection to a point
		#No magic here jsut linear algebra
	def apply(self, position):
		relpos = np.dot(self.Translation,position)
		relpos = np.dot(self.Rotation,relpos)
		renderpos =np.dot(self.Projection,relpos)
		return relpos, renderpos

		#This gives back the unit vector in which the camera points
	def getunit(self):
		return np.dot(GL.CamRot(self.angles),np.array([0,0,-1,0]))[:3]

#Better CAm to be used with BetterAirplane
class BetterCam(Camera):
	def __init__(self,pos,rot,width,height):
		#becuase we have the position and rotation
		#of the cam in the world frame, but we need to
		#transform the world angainst the camera so negative all of it
		self.Translation = GL.TranslateNeg(pos)
		self.Rotation = rot
		self.Projection = GL.Projection(width/height,60,0.1,3000)

#This provides a base for all renderable objects
#Real Object Oriented Languages, would have the pussybility
#to make this classes mathods virtual, and the class abstract.
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

	#We need this very important, otherwise we can no make war in middle east
	def IsHeBush(self, pos):
		return False


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
				x = (1+renderpos[0])*width/2/renderpos[2]
				y = (1-renderpos[1])*height/2/renderpos[2]
				# now we cutoff if its outside the screen, because that saves time
				if 0<=x<=width and 0<=y<=height:
					pygame.draw.circle(screen,l.colour,(int(x),int(y)),1)

#We make a WTC we can crash into
#we make it inherit from the runway so we dont have to rewrite the render function
class WTC(Runway):
	def __init__(self,offpos,offrot):
		self.lights = []
		self.pos = [offpos[0,3],offpos[2,3]]

		#make many floors floors
		for i in range(50):
			positions = [[0,0],[0,5],[0,10],[0,15],[0,20],[5,20],[10,20],[15,20],[20,20],
						[20,15],[20,10],[20,5],[20,0],[15,0],[10,0],[5,0]]
			#just appen all of them		
			for p in positions:
				tmppos = np.array([p[0],7*i,p[1],1])
				self.lights.append(light(offpos.dot(offrot).dot(tmppos),(255,255,255)))

		#And make antenna
		for i in range(50,70):
			tmppos = np.array([10,7*i,10,1])
			self.lights.append(light(offpos.dot(offrot).dot(tmppos),(255,0,0) if i % 2 == 0 else (255,255,255)))

	#check if you are already in the tower
	#Display a bush picture then
	#But psscht its top secret
	def IsHeBush(self, cpos):
		return ((self.pos[0]<=cpos[0]<=self.pos[0]+20) and (self.pos[1]<=cpos[2]<=self.pos[1]+20)) and 0<=self.pos[1]<=7*50

class Horizon(GameObject):
	def setpos(self, cpos):
		self.r = sqrt(2*6371000)*sqrt(abs(cpos[1]))
		self.p = np.array([cpos[0],cpos[1]])

	def __init__(self, cpos):
		self.setpos(cpos)

	def update(self, cpos):
		self.setpos(cpos)

	#sadly we cant use the old render method so just make a new one
	def render(self, screen, cam, width, height):
		
		ps = []
		for angle in range(0,360,20):
			a = radians(angle)
			tmp = self.p + GL.Rot2D(a).dot(np.array([self.r,0]))
			ps.append(np.array([tmp[0],0,tmp[1],1]))

		renders = []
		for d in ps:
			relpos, renderpos = cam.apply(d)
			renderpos = renderpos/renderpos[3]
			#then we make it to x,y space and invert y because python is a
			#special child
			x = (1+renderpos[0])*width/2/renderpos[2]
			y = (1-renderpos[1])*height/2/renderpos[2]
			if relpos[2] < 0 and -400<=x<=width+400 and -400<=y<=height+400:
				renders.append((x,y))

		for i in range(len(renders)-1):
			pygame.draw.line(screen, (0,255,0),renders[i],renders[i+1],1)



#quick mockup nigga
plane = BetterAirplane(np.array([-40,200,400]))

width = 800
height = 500

pygame.init()
screen = pygame.display.set_mode((width,height))

scene = Scene()
cam = BetterCam(plane.pos,plane.getrot(),width,height)
#if you dont want to have the runway transformed give it 4*4 Identity matrixes
#If you have patience and a fucking strong pc, you could build the whole world outta it
scene.objects.append(Runway(np.identity(4),np.identity(4)))
scene.objects.append(Runway(GL.Translate([50,0,20]),GL.Roty(-30)))
scene.objects.append(WTC(GL.Translate([-100,0,0]),np.identity(4)))
scene.objects.append(WTC(GL.Translate([-150,0,0]),np.identity(4)))
scene.objects.append(Horizon(plane.pos))

img = pygame.image.load("george-bush.bmp")
myfont = pygame.font.SysFont("monospace", 23)
myfont2 = pygame.font.SysFont("monospace", 10)
bush = False

lastt = 0
while True:
	curt = pygame.time.get_ticks()

	dt = (curt-lastt)/1000 #makey makey deytey

	cam = BetterCam(plane.pos,plane.getrot(),width,height)
	plane.move(dt)
	screen.fill((15,15,15))
	scene.render(screen, cam, width, height)

	#leave in or Sybrand will visit you
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	#For the stuff thing
	for p in scene.objects:
		if p.IsHeBush(plane.pos) or bush:
			tmp = img.get_rect().size
			bush = True
			screen.blit(img,(width/2-tmp[0]/2,height/2-tmp[1]/2))
			screen.blit(myfont.render("Bush want's to know your Location",1,(255,0,0)),(width/2-tmp[0]/2-75,height/2+tmp[1]/2))
			break

	#there  must be a better way to do this, but im not that good with python
	#so i'll leave it like this
	for i in range(len(scene.objects)):
		if type(scene.objects[i]) == type(Horizon(plane.pos)):
			scene.objects[i].update(plane.pos)

	#Stuff to control
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		plane.pitch(1)
	if keys[pygame.K_s]:
		plane.pitch(-1)

	if keys[pygame.K_a]:
		plane.yaw(1)
	if keys[pygame.K_d]:
		plane.yaw(-1)

	if keys[pygame.K_q]:
		plane.roll(1)
	if keys[pygame.K_e]:
		plane.roll(-1)

	if keys[pygame.K_UP]:
		plane.acc += 1
	if keys[pygame.K_DOWN]:
		plane.acc -= 1

	screen.blit(myfont2.render("Please don't fly sick da loops",1,(0,255,255)),(10,10))
	pygame.display.update()
	lastt = curt
