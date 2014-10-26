#
# a game by Adam Binks

import pygame, random

class GameHandler:
	def __init__(self, data):
		data.newGame()

		# TEMP
		data.level = Level(data, 'dirt')
		data.level.loadRoom(data, 'test')


	def update(self, data):
		data.gameSurf.blit(data.level.surf, (0, 0))
		data.screen.blit(data.gameSurf, data.gameRect)



class Level:
	terrainTypes = ['grass', 'dirt', 'stone', 'barrel', 'crate']
	def __init__(self, data, bgCellTerrain):
		self.loadTerrainImages(data)
		self.bgCellTerrain = bgCellTerrain


	def loadRoom(self, data, roomName):
		self.genRoom(data)
		self.genSurf(data)


	def genRoom(self, data):
		"""Generates a 2d list self.room containing strings of what terrain type is in each cell"""
		self.room = []
		for x in range(data.XCELLS):
			column = []
			for y in range(data.YCELLS):
				column.append(random.choice(['dirt', 'dirt', 'dirt', 'crate', 'barrel']))
			self.room.append(column)


	def genSurf(self, data):
		self.surf = pygame.Surface(data.ROOMSIZE)
		for x in range(data.XCELLS):
			for y in range(data.YCELLS):
				self.surf.blit(self.terrainSurfs[self.bgCellTerrain], (x * data.CELLSIZE, y * data.CELLSIZE))
				self.surf.blit(self.terrainSurfs[self.room[x][y]], (x * data.CELLSIZE, y * data.CELLSIZE))


	# def getTilesetNumberForTile(self, tileCoords):
	# 	"""
	# 	Returns a number which corresponds to the image that should be used.
	# 	More info :http://www.saltgames.com/2010/a-bitwise-method-for-applying-tilemaps/
	# 	"""
	# 	pass


	def loadTerrainImages(self, data):
		self.terrainSurfs = {}
		for terrain in Level.terrainTypes:
			self.terrainSurfs[terrain] = data.loadImage('assets/terrain/%s.png' %(terrain))