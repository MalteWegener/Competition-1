"""
This file just provides some basic 3D matrices, for the render engine
Please dont touch other wise the game will fuck up harder than you in thermo
if you want to get some nice reading on 3d projection,
go to:
https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/projection-matrix-introduction
If you dont understand just use it
its just linear algebra
"""

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

def CamRot(r):
	return Rotz(r[2]).dot(Rotx(r[0])).dot(Roty(r[1]))

def Rot(r):
	return Rotx(r[0]).dot(Roty(r[1])).dot(Rotz(r[2]))