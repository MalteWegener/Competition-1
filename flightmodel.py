from math import *
import numpy as np
#Yo bro, like an airplane is pretty complicated,
#because it can rotate harder than a washing machine
#Please don't fly loops
#Im not ganna add numerical integration for now, do that yourself
#I'm not your bitch
class Airplane():
	def __init__(self, pos):
		self.pos = np.array(pos)
		self.rot = np.zeros([3])
		self.v = 40
		self.acc = 0

	def pitch(self, angle):
		self.rot = self.rot + np.array([angle,0,0])#np.array([angle * cos(self.rot[2]),angle * sin(self.rot[2]),0])
		
	def yaw(self, angle):
		self.rot = self.rot + np.array([0,angle,0])#np.array([angle * sin(self.rot[2]),angle*cos(self.rot[2]),0])

	def roll(self, angle):
		self.rot = self.rot + np.array([0,0,angle])

	def move(self, unit, dt):
		self.v += self.acc*dt
		self.pos = self.pos + dt * self.v * unit