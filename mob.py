# 
# a game by Adam Binks

import pygame

from component import MovementComponent


class Soldier(pygame.sprite.Sprite):
	def __init__(self, data, topleft):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.soldiers)

		self.image = data.loadImage('assets/mobs/soldier.png')
		self.rect = self.image.get_rect(topleft = topleft)

		self.speed = 10

		self.movement = MovementComponent(self, True)
		self.destination = (50, 30) # TEMP


	def update(self, data):
		self.movement.update(data)
		data.gameSurf.blit(self.image, self.rect)