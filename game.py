#
# a game by Adam Binks

import pygame, random
from mob import Soldier, Player

class GameHandler:
	def __init__(self, data):
		data.newGame()

		# TEMP
		data.level = Level(data, 'dirt')
		roomPool = data.level.loadFloorRoomsPatterns('testFloor')
		data.level.loadRoom(data, roomPool)



	def update(self, data):
		data.gameSurf.blit(data.level.surf, (0, 0))

		data.soldiers.update(data)
		data.players.update(data)
		data.dynamicObjects.update(data)

		data.screen.blit(data.gameSurf, data.gameRect)



class Level:
	terrainTypes = ['grass', 'dirt', 'stone', 'barrel', 'crate']
	passableTerrainTypes = ['dirt', 'grass']
	terrainTypeLevelFileCodes = {'G': 'grass', ' ': 'dirt', 'S': 'stone', 'B': 'barrel', 'C': 'crate'}
	def __init__(self, data, bgCellTerrain):
		self.loadTerrainImages(data)
		self.bgCellTerrain = bgCellTerrain


	def loadRoom(self, data, roomPool):
		self.genRoom(random.choice(roomPool), data)
		self.genSurf(data)


	def genRoom(self, roomCells, data):
		"""Generates a 2d list self.room containing strings of what terrain type is in each cell"""
		self.room = []
		data.nodes = []

		for x in range(data.XCELLS):
			column = []
			for y in range(data.YCELLS):
				cellCode = roomCells[y][x]
				if cellCode in Level.terrainTypeLevelFileCodes.keys():
					cellType = Level.terrainTypeLevelFileCodes[cellCode]
				else:
					cellType = 'dirt'
				column.append(cellType)

				# TEMP - player/soldier will appear in doorway
				if cellType == 'dirt' and len(data.soldiers) == 0:
					Soldier((x, y), data)
					Player((x, y), data)

				data.nodes.append(Node((x, y), cellType in Level.passableTerrainTypes))

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


	def loadFloorRoomsPatterns(self, filename):
		"""Loads all the possible rooms for designated floor"""
		roomsFile = open('assets/levels/%s.txt' %(filename), 'r')
		roomsFile = list(roomsFile)

		rooms = []
		lastEnd = 0
		for i in range(len(roomsFile)):
			if 'END' in roomsFile[i]:
				rooms.append(roomsFile[lastEnd:i-1])
				lastEnd = i + 1

		return rooms


	def coordIsPassable(self, coord):
		"""Returns True if the given coordinate can be walked through, else returns False"""
		return self.room[coord[0]][coord[1]] in Level.passableTerrainTypes



class Node:
	"""A simple container for some data used in pathfinding"""
	def __init__(self, coords, passable):
		"""Passable = can be walked over/through"""
		self.coords = coords
		self.passable = passable


	def resetValues(self):
		"""Reset values for a new path to be found"""
		self.previous = None
		self.cost = 99999999999999999999999