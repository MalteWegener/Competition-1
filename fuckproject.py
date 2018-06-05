sections = [[2,2,3],[3,2,4],[3,4,5],[3,4,6]]
Inertia = []
NA =[]
x =[0.3,0.645,1.1,1.5*4/3]

Inertiathin = 0.0015**3*0.0001/12+0.0015*0.0001**3/12
AreaThin = 2*0.0015*0.0001

Inertiathick = 0.0015**3*0.00015/12+0.0015*0.00015**3/12
AreaThick = 2*0.0015*0.00015

InertiaBox = 2*0.15**3*0.0008/12*2*0.0008**3*0.4+0.8*0.0008*2*0.075**2
Areabox = 0.0008*(0.8*0.3)

for s in sections:
	Atop = s[0]*AreaThin+s[1]*AreaThick
	Abot = s[2]*AreaThick
	Q = Atop*0.15+Areabox*0.075
	NA.append(Q/(Atop+Abot+Areabox))
	Inertia.append(s[0]*Inertiathin+(s[1]+s[2])*Inertiathick+Areabox*(NA[-1]-0.075)**2+Atop*(0.15-NA[-1])**2+Abot*(NA[-1])**2+InertiaBox)

stresses = []

for i in range(len(NA)):
	stresses.append(2500*x[i]*(0.15-NA[i]/Inertia[i])/10**6*-1)

print(stresses)