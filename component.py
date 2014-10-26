# 
# a game by Adam Binks

import pygame

class MovementComponent:
	"""Handles basic movement in 8 directions"""
	def __init__(self, master, usePathfinding):
		self.master = master
		self.master.trueCoords = list(self.master.rect.topleft)

		self.master.xVel = self.master.yVel = 0
		self.master.destination = self.master.trueCoords

		if usePathfinding:
			pass  # INIT PATHFINDING STUFF


	def update(self, data):
		if self.master.destination != self.master.rect.topleft:
			move = [0, 0]  # should move R/L and UP/DOWN?

			roughCoords = self.master.rect.topleft
			for axis in (0, 1):
				if roughCoords[axis] < self.master.destination[axis]:
					move[axis] = 1
				if roughCoords[axis] > self.master.destination[axis]:
					move[axis] = -1


			if move[0] != 0 and move[1] != 0: # if moving diagonally move 1/2 distance in each direction
				moveSpeed = self.master.speed / 2.0
			else:
				moveSpeed = self.master.speed

			for axis in (0, 1):
				self.master.trueCoords[axis] += move[axis] * moveSpeed * data.dt

		self.master.rect.topleft = self.master.trueCoords


	def goToCoords(self, coords, data):
		pass
