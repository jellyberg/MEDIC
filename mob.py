# 
# a game by Adam Binks

import pygame, random

from component import MovementComponent, CollisionComponent


class Player(pygame.sprite.Sprite):
	def __init__(self, coords, data):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.players)
		self.add(data.friendlyMobs)

		self.image = data.loadImage('assets/mobs/player.png')
		self.rect = self.image.get_rect(topleft = data.cellToPix(coords))
		self.trueCoords = list(coords)

		self.collision = CollisionComponent(self)

		self.speed = 10


	def update(self, data):
		self.move(data)
		self.collision.updateWorldCollision(data)

		data.gameSurf.blit(self.image, self.rect)
		print str(self.rect.topleft)


	def move(self, data):
		move = [0, 0]
		for direction in ['up', 'down', 'left', 'right']:
			if data.keybinds['move%s' %(direction.capitalize())] in data.input.pressedKeys:
				if direction == 'left':
					move[0] = -self.speed
				if direction == 'right':
					move[0] = self.speed
				if direction == 'up':
					move[1] = -self.speed
				if direction == 'down':
					move[1] = self.speed

		for axis in (0, 1):
			self.trueCoords[axis] += move[axis] * data.dt
		self.rect.topleft = self.trueCoords




class Soldier(pygame.sprite.Sprite):
	def __init__(self, coords, data):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.soldiers)
		self.add(data.friendlyMobs)

		self.image = data.loadImage('assets/mobs/soldier.png')
		self.rect = self.image.get_rect(topleft = data.cellToPix(coords))

		self.speed = 10

		self.movement = MovementComponent(self, True)


	def update(self, data):
		if not self.movement.path:
			self.movement.goToCoords((random.randint(0, data.XCELLS - 1), random.randint(0, data.YCELLS - 1)), data)

		self.movement.update(data)
		data.gameSurf.blit(self.image, self.rect)