from math import *
import numpy as np
#Yo bro, like an airplane is pretty complicated,
#because it can rotate harder than a washing machine
class Airplane():
	def __init__(self, pos):
		self.pos = np.array(pos)
		self.rot = np.zeros([3])

	#up is positive becuase im the best motherfucker
	def pitch(self, angle):
		self.rot = self.rot + np.array([angle,0,0])#np.array([angle * cos(self.rot[2]),angle * sin(self.rot[2]),0])
		
	#left is positive
	def yaw(self, angle):
		self.rot = self.rot + np.array([0,angle,0])#np.array([angle * sin(self.rot[2]),angle*cos(self.rot[2]),0])

	def roll(self, angle):
		self.rot = self.rot + np.array([0,0,angle])