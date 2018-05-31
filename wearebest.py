import numpy as np

filedirs = open("F://Downloads//Compression testing E10//f.txt").readlines()
for i in range(len(filedirs)):
	filedirs[i] = filedirs[i].replace("\n","")
	filedirs[i] += "//specimen.dat"

files = []
for d in filedirs:
	files.append(open(d,encoding="UTF-8").readlines())

dat =[]
for f in files:
	tmp = []
	for i in range(10,len(f)):
		try:
			tmp.append(float(f[i].replace("\n","").split("\t")[1].replace(",",".")))
		except:
			b = 1
	dat.append(min(tmp))

names = []
for f in filedirs:
	names.append(f.split("//")[-2].split("-")[0])

for i in range(len(dat)):
	print(names[i],":",dat[i]*-4.44822-30000) if dat[i]*-4.44822-30000 > 0 else print("",end="")