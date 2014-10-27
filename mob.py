# 
# a game by Adam Binks

import pygame, random

from component import MovementComponent


class Soldier(pygame.sprite.Sprite):
	def __init__(self, coords, data):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.soldiers)

		self.image = data.loadImage('assets/mobs/soldier.png')
		self.rect = self.image.get_rect(topleft = data.cellToPix(coords))

		self.speed = 10

		self.movement = MovementComponent(self, True)


	def update(self, data):
		if not self.movement.path:
			self.movement.goToCoords((random.randint(0, data.XCELLS - 1), random.randint(0, data.YCELLS - 1)), data)

		self.movement.update(data)
		data.gameSurf.blit(self.image, self.rect)