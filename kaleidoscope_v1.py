# Kaleid0scope - inspired by: https://i.imgur.com/pbkgUBv.gifv
# @TheWorldFoundry

# Select a triangular area from an image
# Flip/rotate and replicate it onto a target image.

import sys
from math import atan2,degrees,sqrt
from random import random,randint
import pygame
from pygame import gfxdraw
pygame.init()

BGCOL = (255,255,255)

def doit():

	FILENAME = "_"+str(randint(1000000000,9999999999))
	imgSource = pygame.image.load(sys.argv[1]+".png")
	height = imgSource.get_width()
	width = height
	imgTarget = pygame.Surface((width, height))
	imgTarget.set_colorkey((0,0,0))
	# Choose a section of the image
	minSize = height>>6
	maxSize = height>>3
	size = randint(minSize,maxSize)
	sizeY = int(sqrt(size**2 - (size/2)**2))-1
	print size,sizeY
	imgFragmentX = randint(0,width-size-1)
	imgFragmentY = randint(0,height-sizeY-1)
	imgFragment = pygame.Surface((size,sizeY))
	imgFragment.set_colorkey((0,0,0))
	imgFragment.blit(imgSource,(0,0,size,sizeY),(imgFragmentX,imgFragmentY,size,sizeY))
	pygame.image.save(imgFragment, sys.argv[1]+FILENAME+"_KaleidoscopeFrag.png")
	# Now we need to mask out only the triangle we care about.
	pointsA = [(0,0),(0,sizeY-1),(size>>1,sizeY-1)]
	pointsA.append(pointsA[0])
	pointsB = [(size-1,0),(size-1,sizeY-1),(size>>1,sizeY-1)]
	pointsB.append(pointsB[0])
	gfxdraw.filled_polygon(imgFragment,pointsA,(0,0,0,255))
  	gfxdraw.filled_polygon(imgFragment,pointsB,(0,0,0,255))
	pygame.image.save(imgFragment, sys.argv[1]+FILENAME+"_KaleidoscopeFragClip.png")
	imgFragmentFlipped = pygame.transform.flip(imgFragment,False,True)
	angle = degrees(atan2(size>>1,sizeY))*2
	imgFragmentRotate1 = pygame.transform.rotate(imgFragmentFlipped,angle*2)
	imgFragmentRotate1rect = imgFragmentRotate1.get_bounding_rect()
	imgFragmentRotate2 = pygame.transform.rotate(imgFragmentFlipped,angle*4)
	imgFragmentRotate2rect = imgFragmentRotate2.get_bounding_rect()
	imgFragmentRotate3 = pygame.transform.rotate(imgFragment,angle*2)
	imgFragmentRotate3rect = imgFragmentRotate3.get_bounding_rect()
	imgFragmentRotate4 = pygame.transform.rotate(imgFragment,angle*4)
	imgFragmentRotate4rect = imgFragmentRotate4.get_bounding_rect()

	# Now we need to blit this into a hex pattern
	imgFragmentHexTile = pygame.Surface((size<<1,sizeY<<1))
	imgFragmentHexTile.set_colorkey((0,0,0))
	x = size>>1
	y = 0
	imgFragmentHexTile.blit(imgFragment,[x,y])
	imgFragmentHexTile.blit(imgFragmentFlipped,[x,y+sizeY],)
	imgFragmentHexTile.blit(imgFragmentRotate1,[x+(size>>1),y],imgFragmentRotate1rect)
	imgFragmentHexTile.blit(imgFragmentRotate1,[x-(size),y+sizeY],imgFragmentRotate1rect)
	imgFragmentHexTile.blit(imgFragmentRotate2,[x-(size>>1),y],imgFragmentRotate2rect)
	imgFragmentHexTile.blit(imgFragmentRotate2,[x+(size),y+sizeY],imgFragmentRotate2rect)
	imgFragmentHexTile.blit(imgFragmentRotate3,[x-(size>>1),y+sizeY],imgFragmentRotate3rect)
	imgFragmentHexTile.blit(imgFragmentRotate3,[x+size,y],imgFragmentRotate3rect)
	imgFragmentHexTile.blit(imgFragmentRotate4,[x+(size>>1),y+sizeY],imgFragmentRotate4rect)
	imgFragmentHexTile.blit(imgFragmentRotate4,[x-(size),y],imgFragmentRotate4rect)
	pygame.image.save(imgFragmentHexTile, sys.argv[1]+FILENAME+"_KaleidoscopeHexTile.png")
	# Now we need to blit this around the screen like a crazy freakazoid
	x = 0
	y = 0
	while y < height+sizeY:
		while x < width+size:
			imgTarget.blit(imgFragmentHexTile,[x,y])
#			imgTarget.blit(imgFragmentHexTile,[x-size-(size>>1),y-sizeY])
			x += size<<1
		y += sizeY<<1
		x = 0
	


	pygame.image.save(imgTarget, sys.argv[1]+FILENAME+"_KaleidoscopeOut.png")

while True:
	doit()
