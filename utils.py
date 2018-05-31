import pygame
import random
import Col2D
from math import *

class GameObject():
	def __init__(self):
		return

	def draw(self):
		return

	def checkCollision(self, other):
		return False

class Rectangle(GameObject):
	"""docstring for Rectangle"""
	def updateVerts(self):
		self.vertices = []
		self.vertices.append([self.pos[0],self.pos[1]])
		self.vertices.append([self.pos[0]+self.size[0],self.pos[1]])
		self.vertices.append([self.pos[0]+self.size[0],self.pos[1]+self.size[1]])
		self.vertices.append([self.pos[0],self.pos[1]+self.size[1]])

	def __init__(self, pos, size, colour):
		self.pos = pos
		self.size = size
		self.colour = colour
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def updatepos(self, newpos):
		self.pos = newpos
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def draw(self, Screen):
		pygame.draw.rect(Screen, self.colour, (self.pos[0],self.pos[1],self.size[0],self.size[1]))

class RegularPolygon(GameObject):
	"""docstring for Rectangle"""
	def updateVerts(self):
		self.vertices = []
		angle = 0+self.delrot
		dang = 2*pi/self.corners
		for i in range(self.corners):
			self.vertices.append([self.pos[0]+sin(angle)*self.size,self.pos[1]+cos(angle)*self.size])
			angle += dang

	def __init__(self, pos, size, colour, corners, delrot):
		self.pos = pos
		self.size = size
		self.colour = colour
		self.corners = corners
		self.delrot = delrot
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def updatepos(self, newpos):
		self.pos = newpos
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def updaterot(self, newrot):
		self.delrot = newrot
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def draw(self, Screen):
		pygame.draw.polygon(Screen, self.colour, self.vertices)

class Bird():
	def __init__(self):
		self.pos = 0
		self.size = (50,50)
		self.speed = 0
		self.img = pygame.image.load("bird.bmp")

	def update(self, dt, Screen, pressed):
		acc = 500
		self.speed += acc *dt

		if pressed:
			print("TRUE")
			self.speed -= 450

		self.pos += self.speed*dt
		if self.pos < 0:
			self.pos = 0
			self.speed /= 5
		if self.pos > 550:
			self.pos = 550
			self.speed = 0

		pygame.draw.rect(Screen, (0,255,0), (300,self.pos,self.size[0],self.size[1]))
		Screen.blit(self.img, (300,self.pos))

class Player:
	def updateVerts(self):
		self.vertices = []
		self.vertices.append([self.pos[0],self.pos[1]])
		self.vertices.append([self.pos[0]+self.size[0],self.pos[1]])
		self.vertices.append([self.pos[0]+self.size[0],self.pos[1]+self.size[1]])
		self.vertices.append([self.pos[0],self.pos[1]+self.size[1]])

	def __init__(self, pos, colour):
		self.pos = pos
		self.size = (50,50)
		self.speed = 0
		self.colour = colour
		self.img = pygame.image.load("bird.bmp")
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)

	def draw(self,Screen):
		pygame.draw.polygon(Screen, self.colour, self.vertices)

	def jump(self,objects):
		onground = False
		for obj in objects:
			if self.shell.checkColl(obj.shell):
				onground = True
				break

		if onground:
			self.speed = -300

	def update(self, dt, objects):
		self.speed += dt * 200
		self.pos = (self.pos[0], self.pos[1] + self.speed * dt)
		self.updateVerts()
		self.shell = Col2D.ConvexShell(self.vertices)
		for obj in objects:
			if self.shell.checkColl(obj.shell) and self.speed > 0:
				self.speed = 0




class Gate():
	def __init__(self):
		self.x = 600
		self.y = random.randint(100,500)
		self.size = random.randint(100,300)
		self.col = (0,0,255)

	def update(self, Screen, dt):
		self.x -= 200*dt
		pygame.draw.rect(Screen, self.col, (self.x,0,30,self.y-self.size/2))
		pygame.draw.rect(Screen, self.col, (self.x,self.y+self.size/2,30,600))

	def collideswithbird(self, birdih):
		isingate = False
		if birdih>self.y-self.size/2 and birdih+50<self.y+self.size/2:
			isingate = True
		isbetween = False
		if 350 >= self.x and 300 <= self.x+30:
			isbetween = True

		if isbetween and not isingate:
			self.col = (255,0,0)
			return True
		else:
			self.col = (0,0,255)
			return False