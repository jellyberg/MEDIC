# 
# a game by Adam Binks

import pygame, math

class MovementComponent:
	"""Handles basic movement in 8 directions"""
	def __init__(self, master, usePathfinding):
		self.master = master
		self.master.trueCoords = list(self.master.rect.topleft)

		self.master.xVel = self.master.yVel = 0
		self.master.destination = self.master.trueCoords

		if usePathfinding:
			self.usePathfinding = True
			self.path = []


	def update(self, data):
		if self.usePathfinding and self.path:
			self.master.destination = data.cellToPix(self.path[0])

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
		if self.usePathfinding and self.path and data.pixToCells(self.master.rect.topleft) == self.path[0]:
			del self.path[0]

		print str(self.path)


	def goToCoords(self, coords, data):
		"""Start going towards specified coords"""
		if self.usePathfinding:
			self.path = []
			startCoords = data.pixToCells(self.master.rect.topleft)
			endCoords = coords

			endNode = 'unspecified'
			for node in data.nodes:
				if node.coords == startCoords:
					startNode = node
				if node.coords == endCoords:
					endNode = node
			if endNode == 'unspecified':
				print 'endNode not found. coords: %s' %(str(endCoords))
				data.input.terminate()
			self.path = self.findPath(startNode, endNode, data)
			
		else:
			self.master.destination = coords


	def findPath(self, startNode, endNode, data):
		"""Use A* pathfinding to find the fastest route from A to B"""
		reachable = [startNode]  # nodes that are reachable but unexplored
		explored = []	# nodes that have been explored

		for node in data.nodes:
			node.resetValues()

		while reachable != []:
			# Choose some node we know how to reach
			node = self.chooseNode(reachable, endNode)

			# If we just got to the goal node, build and return the path
			if node == endNode:
				return self.buildPath(endNode)

			# Don't repeat ourselves
			reachable.remove(node)
			explored.append(node)

			# Where can we get from here that we haven't explored before?
			newReachable = list(set(self.getAdjacentNodes(node, data)) - set(explored))
			for adjacent in newReachable:
				# If this is a new path, or a shorter path than what we have, keep it
				if adjacent not in reachable or node.cost + 1 < adjacent.cost:
					adjacent.previous = node
					adjacent.cost = node.cost + 1

				# First time we see this node?
				if adjacent not in reachable:
					reachable.append(adjacent)


		# If we get here, no path was found
		print 'no path found'
		return None


	def chooseNode(self, reachable, endNode):
		"""Choose the next node from reachable nodes to explore"""
		minCost = 9999999999999999999999999999999999999999999999999999999999
		bestNode = None

		for node in reachable:
			costStartToNode = node.cost
			costNodeToGoal = self.estimateDistance(node, endNode)
			totalCost = costStartToNode + costNodeToGoal

			if minCost > totalCost:
				minCost = totalCost
				bestNode = node

		return bestNode


	def buildPath(self, toNode):
		"""Build self.path: a list of coordinates to follow to reach the destination"""
		path = []
		while toNode is not None:
			path = [toNode.coords] + path  # add the coords to the start of the path
			toNode = toNode.previous
		print str(path)
		return path


	def estimateDistance(self, startNode, endNode):
		"""Manhattan distance between startNode and endNode as the crow flies (in a zigzag. it's a drunk crow.)"""
		x1, y1 = startNode.coords
		x2, y2 = endNode.coords
		return math.fabs(x1 - x2) + math.fabs(y1 - y2)


	def getAdjacentNodes(self, node, data):
		"""Returns a list of adjacent passable nodes (no diagonals)"""
		x, y = node.coords
		possibleCoords = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

		adjacent = []
		for node in data.nodes:
			if node.passable:
				for adjCoord in possibleCoords:
					if node.coords == adjCoord:
						adjacent.append(node)

		return adjacent