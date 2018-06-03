import numpy as np
from math import *

def Projection(aspect,fov,near,far):
	Proj = np.zeros([4,4])
	Proj[0,0] = 1/(aspect*tan(radians(fov)/2))
	Proj[1,1] = 1/tan(radians(fov)/2)
	Proj[2,2] = -(far+near)/(far-near)
	Proj[2,3] = -2*(far+near)/(far-near)
	Proj[3,2] = -1
	return Proj

def Translate(off):
	matTrans = np.identity(4)
	matTrans[0,3] = off[0]
	matTrans[1,3] = off[1]
	matTrans[2,3] = off[2]
	return matTrans

def TranslateNeg(off):
	matTrans = np.identity(4)
	matTrans[0,3] = -off[0]
	matTrans[1,3] = -off[1]
	matTrans[2,3] = -off[2]
	return matTrans

def Rotx(t):
	t = radians(t)
	Rot = np.zeros([4,4]) 
	Rot[0,0] = 1
	Rot[3,3] = 1
	Rot[1,1] = cos(t)
	Rot[2,2] = cos(t)
	Rot[1,2] = -sin(t)
	Rot[2,1] = sin(t)
	return Rot

def Roty(t):
	t = radians(t)
	Rot = np.zeros([4,4]) 
	Rot[1,1] = 1
	Rot[3,3] = 1
	Rot[0,0] = cos(t)
	Rot[0,2] = sin(t)
	Rot[2,0] = -sin(t)
	Rot[2,2] = cos(t)
	return Rot

def Rotz(t):
	t = radians(t)
	Rot = np.zeros([4,4]) 
	Rot[2,2] = 1
	Rot[3,3] = 1
	Rot[0,0] = cos(t)
	Rot[0,1] = -sin(t)
	Rot[1,0] = sin(t)
	Rot[1,1] = cos(t)
	return Rot

def Rot(r):
	return Rotz(r[2]).dot(Rotx(r[0])).dot(Roty(r[1]))