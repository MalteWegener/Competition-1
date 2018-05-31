import numpy as np
from numpy.linalg import solve,norm
import pygame 
import sys
from random import randint

def updateObject(line, Ball):
	#assign references for the variables
	#Like every fucking good language could do some kind of passing by ref, so we dont litter up ram
	#but our special Kid python is like nah i wont do that im so cool
	#Writing Python Code is like vaping. YOu think you are cool, but in reality you just inhale water vapour,
	#that tastes like Water melon, You think you program, but in reality you dont do more then just writing coloured
	#pseudo code
	a = np.array(line.vertices[0])
	b = np.array(line.vertices[1])
	p = np.array(Ball.pos)
	q = np.array(Ball.nextpos)

	abn = (b-a)/norm(b-a) #we need abn later

	#make your matrix
	A = np.zeros([2,2])
	A[:,0]=b-a
	A[:,1]=p-q
	#solve it
	#Handle the Parralel case
	try:
		#mu stands for muving
		lam,mu = solve(A,p-a)
	except:
		return False, Ball.nextpos, Ball.v

	#exit if no intersect between 0 and 1
	eps = 0.01
	if (-eps<lam<1+eps and 0<mu<1):
		print()
	else:
		return False, q, Ball.v

	#get intersection point
	S = p + mu*(q-p)
	#get normal vector
	n = np.array([abn[1],-abn[0]])
	if np.dot(q-p,n) > 0:
		n*=-1

	#do some quick maffs like if you dont understand you probablyu are an architect
	v = np.array(Ball.v)
	vn = (abn*abn.dot(v)-n*n.dot(v))
	return True, S+abn*abn.dot(q-S)-n*n.dot(q-S), vn/norm(vn)*norm(v)

"""How the hell can that shit langugae call itself object oriented, if it doesnt know the basic concept
of encapsulation. Python classes are like that weird uncle, who wants everyone to access his private members.
Like no fucking way this language should be allowed to be called object oriented. HASHTAG Shit language
"""
#This class is self documenting
class Line:
	def __init__(self, pos1, pos2):
		self.vertices = [np.array(pos1),np.array(pos2)]

	def render(self, screen):
		pygame.draw.line(screen,(0,255,255),(self.vertices[0][0],self.vertices[0][1]),(self.vertices[1][0],self.vertices[1][1]))

class Ball:
	def __init__(self, pos, v, radius, colour):
		self.pos = np.array(pos)
		self.v = np.array(v)
		self.radius = radius
		self.colour = colour

	def update(self, acc, screen, lines, dt,t):
		acc = np.array(acc)
		self.v = self.v+acc*dt
		self.nextpos = self.pos + self.v *dt
		#check for bouncing with each line
		for line in lines:
			bounce, tmppos, tmpv = updateObject(line, self)
			#if it bounces we update the ball and leave the loop
			if bounce:
				self.pos = tmppos
				self.v = tmpv
				print("Boing "+str(t)+" s "+str(0.5*norm(self.v)**2+(600-self.pos[1])*100)+" J")
				break
			#if not bouncing but we checked last thing then we also update
			elif line is lines[-1]:
				self.pos = tmppos
				self.v = tmpv

		#Then we draw the ball
		p = self.pos #this is just to make the next line shorter
		pygame.draw.circle(screen,self.colour, (int(p[0]),int(p[1])), self.radius)


#------------------------------Main Code--------------------------------
#First we make a screen
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

#Then we make all our bouncy surfaces
#You can always add more
surfs = []
surfs.append(Line((1,1),(1,height-1)))
surfs.append(Line((1,height-1),(width-1,height-1)))
surfs.append(Line((width-1,height-1),(width-1,1)))
surfs.append(Line((1,1),(width-1,1)))
surfs.append(Line((width/2,1),(width/4,height/2)))

#Then make all balls because we are like real fucking nigga badass fuckers
balls = []#Of steel

#make 10 random balls
for i in range(1):
	balls.append(Ball((randint(10,width-10),randint(10, height-10)),(randint(-150,150),randint(-150,150)),5,(randint(0,255),randint(0,255),randint(0,255))))

#For our Framerate counter
myfont = pygame.font.SysFont("monospace", 30)

#now that we got that outta the way we do cool stuff
lastt = pygame.time.get_ticks()
while True:
	#Some necessary stuff to clear the screen and get correct dt
	currentt =pygame.time.get_ticks()
	dt = (currentt-lastt)/1000
	screen.fill((0,0,0))

	#Leave this in otherwise it crashes like your grades
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	#Go through all the balls and update them
	for i in range(len(balls)):
		#So we just call the update for all the balls
		balls[i].update([0,100],screen,surfs,dt,currentt/1000)

	#Draw all lines
	for sf in surfs:
		sf.render(screen)

	#Thats self explanatory
	lastt = currentt
	#Framerate
	#screen.blit(myfont.render(str(round(1/dt if dt > 0 else 60)), 1, (255,255,0)), (50, 50))
	screen.blit(myfont.render(str(sum([0<=b.pos[0]<=width and 0<=b.pos[1]<=height for b in balls])), 1, (255,255,0)), (50, 50))
	pygame.display.update()
	#clock.tick(30) #warning hiogh framerates may result in the loss of balls(Fixed this shit actually)