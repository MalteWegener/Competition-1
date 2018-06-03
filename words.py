wds = set([])

text = open("text.txt").readlines()

for l in text:
	p = l.split()
	for i in p:
		if i not in wds:
			wds.add(i)

print(len(wds))