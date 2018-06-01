import numpy as np
import pygame
from math import *

class Camera(object):
	def __init__(self, pos, rot):
		fov = 125
		near = 0.1
		far = 3000

		self.Proj = np.zeros([4,4])
		self.Proj[0,0] = 1/tan(radians(fov)/2)
		self.Proj[1,1] = 1/tan(radians(fov)/2)
		self.Proj[2,2] = -(far+near)/(far-near)
		self.Proj[2,3] = -2*(far+near)/(far-near)
		self.Proj[3,2] = -1

		self.Matrix = self.Proj.dot(pos).dot(rot)

	def update(self,pos,rot):
		self.Matrix = self.Proj.dot(pos).dot(rot)


class Runway:
	def __init__(self, off, rot):
		lines = open("runway_lights-1.dat").readlines()
		self.lights = []
		self.lightscolour = []
		for l in lines:
			if l is not lines[0]:
				tmp = l.replace("\n","").split(",")
				self.lights.append(off.dot(np.array([float(tmp[0]),0,-float(tmp[1]),1])).dot(rot))
				self.lightscolour.append((float(tmp[2]),float(tmp[3]),float(tmp[4])))

	def render(self, Camera):
		points = []
		for l in self.lights:
			points.append((l.dot(Camera.Matrix)/l.dot(Camera.Matrix)[-1]))

		for p in points:
			print(p)

cm = Camera(np.identity(4),np.identity(4))
rw = Runway(np.identity(4),np.identity(4))
rw.render(cm)