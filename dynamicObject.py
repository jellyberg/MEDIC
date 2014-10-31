# 
# a game by Adam Binks

import pygame, math

class Heal(pygame.sprite.Sprite):
	"""A projectile that disappears when it hits anything. If fit hits a soldier, it restores some HP"""
	def __init__(self, pos, speed, direction, range, data):
		"""Velocity is a tuple (x velocity, y velocity)"""
		pygame.sprite.Sprite.__init__(self)
		self.add(data.dynamicObjects)
		self.add(data.heals)

		self.image = Heal.image
		self.rect = self.image.get_rect(center=pos)
		self.trueCoords = list(self.rect.topleft)

		self.velocity = (direction[0] * speed, direction[1] * speed)
		self.range = range
		self.startCoords = pos


	def update(self, data):
		for axis in (0, 1):
			self.trueCoords[axis] += self.velocity[axis] * data.dt
			if math.fabs(self.trueCoords[axis] - self.startCoords[axis]) > self.range:
				self.kill()
		self.rect.topleft = self.trueCoords

		data.gameSurf.blit(self.image, self.rect)