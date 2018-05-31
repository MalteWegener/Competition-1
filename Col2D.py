import numpy as np

class ConvexShell(object):
	"""docstring for Convex Vertex"""
	def __init__(self, points):
		self.verts = []
		for pt in points:
			self.verts.append(np.array(pt))

	def gettangentVectors(self):
		vecs = []
		for i in range(len(self.verts)):
			temp = self.verts[i]-self.verts[i-1]
			x = temp[0]
			y = temp[1]
			vecs.append(np.array([y,-x]))

		return vecs

	def checkColl(self, other):
		vecs = self.gettangentVectors()
		vecs += other.gettangentVectors()

		"""
		In order to check for collision of 2D convex solid objects, we first reduce the problem to overlap in 1D
		"""
		collisions = []
		for vec in vecs:
			#find max and min dotproducts for each shape and check for overlap
			ownproj = []
			for pt in self.verts:
				ownproj.append(np.dot(vec,pt))
			ownmin = min(ownproj)
			ownmax = max(ownproj)

			otherproj = []
			for pt in other.verts:
				otherproj.append(np.dot(vec,pt))
			othermin = min(otherproj)
			othermax = max(otherproj)

			collisions.append((ownmax >= othermin) and (othermax >= ownmin))
		
		for c in collisions:
			if not c:
				return False


		return True

	def checkPoint(self, point):
		vecs = self.gettangentVectors()

		pot = np.array(point)
		collisions = []
		for vec in vecs:
			ownproj = []
			for pt in self.verts:
				ownproj.append(np.dot(vec,pt))
			ownmin = min(ownproj)
			ownmax = max(ownproj)

			otherproj = np.dot(vec,pot)

			collisions.append((otherproj >= ownmin) and (otherproj <= ownmax))

		for c in collisions:
			if not c:
				return False


		return True

