# define an objective function


bw = bh = 512
w = h = 1

sw = bw*w
sh = bh*h

import pygame
import pygame.camera
from time import sleep
import numpy as np
from hyperopt import fmin, tpe, space_eval, hp
import hyperopt
from colorsys import hsv_to_rgb

pygame.camera.init()
print(pygame.camera.list_cameras())

cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
sleep(0.1)

def grabImageAverage():
	img = cam.get_image()
	#pygame.image.save(img, "webcam.jpg")
	data = pygame.surfarray.array3d(img)

	#print(data)
	mean = np.mean(data, axis=(0, 1))
	print(mean)
	r,g,b = mean
	#brightness = sum(mean)#
	return -(r+g+b)#-(r-g-b)

pygame.init()
pygame.display.set_caption("spacesearch")

screen = pygame.display.set_mode((sw,sh))
screen.fill((255, 255, 255))

def objective(args):

	for y in range(h):
		for x in range(w):
			index = y*w+x
			pixel = args[index]
			rgb = hsv_to_rgb(*pixel)
			rgb = [int(v*255) for v in rgb]
			#pixel = [int(p) for p in pixel]
			#print(rgb)
			pygame.draw.rect(screen, rgb, pygame.Rect(x*bw, y*bh, bw, bh))

	"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	"""

	pygame.display.flip()
	#sleep(0.1)

	score = grabImageAverage()

	return score

# define a search space


space = []



i = 0
for y in range(h):
	for x in range(w):
		si = str(i)
		#space.append([hp.quniform("r-"+si, 0, 255, 1), hp.quniform("g-"+si, 0, 255, 1), hp.quniform("b-"+si, 0, 255, 1)])
		#space.append([hp.uniform("r-"+si, 0, 255), hp.uniform("g-"+si, 0, 255), hp.uniform("b-"+si, 0, 255)])
		space.append([hp.uniform("r-"+si, 0, 1), hp.uniform("g-"+si, 0, 1), hp.uniform("b-"+si, 0, 1)])
		i += 1

# minimize the objective over the space




#hyperopt.rand.suggest
best = fmin(objective, space, algo=tpe.suggest, max_evals=1000)

print(best)
# -> {'a': 1, 'c2': 0.01420615366247227}
print(space_eval(space, best))
# -> ('case 2', 0.01420615366247227}
