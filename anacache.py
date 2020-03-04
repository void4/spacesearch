import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

with open("cache-1583326076636") as cachefile:
	cache = json.loads(cachefile.read())

print(list(cache.items())[0])

x = []
y = []
c = []
s = []

bodies = {
	"thin": 0.5,
	"sporty": 0.8,
	"normal": 1,
	"chubby": 1.2,
	"fat": 1.4
}

"""
colors = {
	"black": (0,0,0),
	"red": (255,0,0),
	"blonde": (255,255,0),
	"bald": (200,200,200),
	"gray": (127,127,127),
	"brown": (255,127,0)
}
"""

cats = defaultdict(list)

for key, value in cache.items():
	key = json.loads(key)
	selector = key["haircolor"]
	x.append(selector)
	y.append(-value)
	cats[selector].append(-value)
	c.append(key["haircolor"].replace("blonde", "yellow"))#colors[key["haircolor"]])
	s.append(bodies[key["body"]]*50)

avg = np.mean(y)

for key, l in cats.items():
	keymean = np.mean(l)
	print(key, keymean, keymean-avg)

print("Average score:", avg)

def approx(params):
	avg = 47.47286012526096
	#fem_height_bonus = 33/(1+abs(175 - params["height"])*1)# * 10/25
	hairdelta = {
		"red": -9.67,
		"black": -9.11,
		"brown": -6.22,
		"gray": -13.73,
		"blonde": 5.34
	}[params["haircolor"]]

	bodydelta = {
		"chubby": 0.82,
		"thin": -2.77,
		"normal": -0.27,
		"fat": 2.22,
		"sporty": -5.06
	}[params["body"]]

	return avg + hairdelta + bodydelta# + fem_height_bonus

error = 0
for key, value in cache.items():
	params = json.loads(key)
	value = -value
	delta = abs(approx(params)-value)
	error += delta

print("Average error:", error/len(cache))
#colors = np.random.rand(N)
#area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
#s=area
plt.scatter(x, y, c=c, s=s, alpha=0.5)
plt.show()
