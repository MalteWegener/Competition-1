from math import *
import numpy as np
import GL
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
		self.rot = self.rot + np.array([angle,0,0])
		
	def yaw(self, angle):
		self.rot = self.rot + np.array([0,angle,0])

	def roll(self, angle):
		self.rot = self.rot + np.array([0,0,angle])

	def move(self, unit, dt):
		self.v += self.acc*dt
		self.pos = self.pos + dt * self.v * unit

#This model may be quite Complicated, but at least we are consistent now
#works best for small angles
class BetterAirplane():
	def __init__(self, pos):
		self.pos = pos
		self.v = 40
		self.yawaxis = np.array([0,-1,0])
		self.pitchaxis = np.array([1,0,0])
		self.rollaxis = np.array([0,0,-1])
		self.acc = 40
		self.maxpitchspeed = 20
		self.maxyawspeed = 15
		self.maxrollspeed = 20

	def pitch(self,angle, dt):
		if angle > 0:
			angle = self.maxpitchspeed*dt
		else:
			angle = -self.maxpitchspeed*dt

		self.yawaxis = GL.UniversalRotationDeg(angle,self.pitchaxis).dot(self.yawaxis)
		self.rollaxis = GL.UniversalRotationDeg(angle,self.pitchaxis).dot(self.rollaxis)

	def pitchabs(self,angle):

		self.yawaxis = GL.UniversalRotationDeg(angle,self.pitchaxis).dot(self.yawaxis)
		self.rollaxis = GL.UniversalRotationDeg(angle,self.pitchaxis).dot(self.rollaxis)

	def yaw(self,angle, dt):
		if angle > 0:
			angle = self.maxyawspeed*dt
		else:
			angle = -self.maxyawspeed*dt

		self.pitchaxis = GL.UniversalRotationDeg(-angle,self.yawaxis).dot(self.pitchaxis)
		self.rollaxis = GL.UniversalRotationDeg(-angle,self.yawaxis).dot(self.rollaxis)

	def roll(self,angle, dt):
		if angle > 0:
			angle = self.maxrollspeed*dt
		else:
			angle = -self.maxrollspeed*dt

		self.yawaxis = GL.UniversalRotationDeg(-angle,self.rollaxis).dot(self.yawaxis)
		self.pitchaxis = GL.UniversalRotationDeg(-angle,self.rollaxis).dot(self.pitchaxis)

	def getrot(self):
		yp = -self.yawaxis
		zp = -self.rollaxis
		xp = self.pitchaxis

		x = np.array([1,0,0])
		y = np.array([0,1,0])
		z = np.array([0,0,1])

		Mat = np.zeros([4,4])
		Mat[3,3] = 1

		Mat[0,0] = np.dot(x,xp)
		Mat[0,1] = np.dot(x,yp)
		Mat[0,2] = np.dot(x,zp)

		Mat[1,0] = np.dot(y,xp)
		Mat[1,1] = np.dot(y,yp)
		Mat[1,2] = np.dot(y,zp)

		Mat[2,0] = np.dot(z,xp)
		Mat[2,1] = np.dot(z,yp)
		Mat[2,2] = np.dot(z,zp)

		#Either Transpose or switch around stuff uptop, but i guessed the right matrix so transpose
		return Mat.transpose()

	def move(self, dt):
		self.v += dt * self.acc
		self.pos = self.pos + self.v*self.rollaxis*dt
		#make landy landy
		if self.pos[1] < 0:
			self.pos[1] = 0