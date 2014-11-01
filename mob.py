# 
# a game by Adam Binks

import pygame, random, time
from component import MovementComponent, CollisionComponent, HealthBar
from dynamicObject import Heal


class Player(pygame.sprite.Sprite):
	baseStats = {'speed': 20, 'fireRate': 0.3, 'healthPerHeal': 20, 'healRange': 320, 
				 'healTravelSpeed': 30, 'health': 'TODO'}
	def __init__(self, coords, data):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.players)
		self.add(data.friendlyMobs)

		self.image = data.loadImage('assets/mobs/player.png')
		self.rect = self.image.get_rect(topleft = data.cellToPix(coords))
		self.trueCoords = list(coords)
		self.velocity = [0, 0]

		self.collision = CollisionComponent(self)

		self.speed = Player.baseStats['speed']
		self.acceleration = 8.0
		self.decceleration = 1.1

		self.healthPerHeal = Player.baseStats['healthPerHeal']
		self.healRange = Player.baseStats['healRange']
		self.healTravelSpeed = Player.baseStats['healTravelSpeed']
		self.fireRate = Player.baseStats['fireRate']

		self.lastShootTime = time.time()


	def update(self, data):
		self.move(data)
		self.collision.updateWorldCollision(data)

		self.checkForShoot(data)

		data.gameSurf.blit(self.image, self.rect)


	def move(self, data):
		hasMoved = [False, False]

		for direction in ['up', 'down', 'left', 'right']:
			if data.keybinds['move%s' %(direction.capitalize())] in data.input.pressedKeys:
				if direction == 'left':
					self.velocity[0] -= self.acceleration * data.dt
					hasMoved[0] = True
				if direction == 'right':
					self.velocity[0] += self.acceleration * data.dt
					hasMoved[0] = True
				if direction == 'up':
					self.velocity[1] -= self.acceleration * data.dt
					hasMoved[1] = True
				if direction == 'down':
					self.velocity[1] += self.acceleration * data.dt
					hasMoved[1] = True

		for axis in (0, 1):
			# DECELERATE IF HAS NOT MOVED THIS FRAME AND IS STILL SKIDDING
			if self.velocity[axis] == 0.0 or hasMoved[axis] == True:
				continue

			self.velocity[axis] = self.velocity[axis] / self.decceleration
			if -1 < self.velocity[axis] < 1:
				self.velocity[axis] = 0

		for axis in (0, 1):
			if self.velocity[axis] > self.speed:
				self.velocity[axis] = self.speed
			if self.velocity[axis] < -self.speed:
				self.velocity[axis] = -self.speed

			self.trueCoords[axis] += self.velocity[axis] * data.dt
		self.rect.topleft = self.trueCoords


	def checkForShoot(self, data):
		"""Reads user input and shoots if a corresponding key is pressed"""
		if time.time() - self.lastShootTime > self.fireRate:
			for direction in ['up', 'down', 'left', 'right']:
				if data.keybinds['shoot%s' %(direction.capitalize())] in data.input.pressedKeys:
					self.shoot(direction, data)
					break
			self.lastShootTime = time.time()


	def shoot(self, direction, data):
		"""Shoots a heal in the specified direction"""
		Heal(self.rect.center, self.healTravelSpeed, data.directionsDict[direction], self.healRange, self.healthPerHeal, data)


class Soldier(pygame.sprite.Sprite):
	def __init__(self, coords, data):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.soldiers)
		self.add(data.friendlyMobs)

		self.image = data.loadImage('assets/mobs/soldier.png')
		self.rect = self.image.get_rect(topleft = data.cellToPix(coords))

		self.speed = 15
		self.maxHealth = 200
		self.health = 20 # self.maxHealth

		self.movement = MovementComponent(self, True)
		self.healthBar = HealthBar(self.maxHealth, data.GREEN, self.rect, data)


	def update(self, data):
		if not self.movement.path:
			self.movement.goToCoords((random.randint(0, data.XCELLS - 1), random.randint(0, data.YCELLS - 1)), data)

		self.movement.update(data)
		data.gameSurf.blit(self.image, self.rect)
		self.healthBar.draw(self.health, self.rect, data)


	def heal(self, amount):
		self.health += amount
