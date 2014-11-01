# 
# a game by Adam Binks
import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)   # use a lower buffersize to reduce sound latency
pygame.init()

import input, game, math
from pygame.locals import *
from dynamicObject import Heal

def run():
	stateHandler = StateHandler()
	while True:
		stateHandler.update()


class StateHandler:
	"""handles menu and game state, runs boilerplate update code"""
	def __init__(self):
		self.data = Data()
		self.data.screen.fill((135, 206, 250))
		pygame.display.set_caption('MEDIC!')

		self.gameHandler = game.GameHandler(self.data)


	def update(self):
		self.data.input.get()
		self.data.dt = self.data.FPSClock.tick(self.data.FPS) / 100.0

		# update game/menu objs
		self.gameHandler.update(self.data)

		pygame.display.update()
		pygame.display.set_caption('MEDIC!  FPS: %s' %(int(self.data.FPSClock.get_fps())))



class Data:
	"""stores variables to be accessed in many parts of the game"""
	def __init__(self):
		screenInfo = pygame.display.Info()
		self.WINDOWWIDTH = screenInfo.current_w
		self.WINDOWHEIGHT = screenInfo.current_h
		self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))#, pygame.locals.FULLSCREEN)

		self.FPSClock = pygame.time.Clock()
		self.FPS = 60
		self.input = input.Input()

		self.keybinds = {'moveUp': K_w, 'moveLeft': K_a, 'moveRight': K_d, 'moveDown': K_s,
						 'shootUp': K_UP, 'shootLeft': K_LEFT, 'shootRight': K_RIGHT, 'shootDown': K_DOWN}

		self.directionsDict = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

		Heal.image = self.loadImage('assets/objects/heal.png')

		self.WHITE     = (255, 255, 255)
		self.BLACK     = (  0,   0,   0)
		self.SKYBLUE   = (135, 206, 250)
		self.DARKBLUE  = (  0,  35, 102)
		self.YELLOW    = (255, 255, 102)
		self.DARKYELLOW= (204, 204,   0)
		self.GREEN     = (110, 255, 100)
		self.ORANGE    = (255, 165,   0)
		self.DARKGREY  = ( 60,  60,  60)
		self.LIGHTGREY = (180, 180, 180)
		self.CREAM     = (255, 255, 204)


	def newGame(self):
		self.XCELLS, self.YCELLS = (24, 12)
		self.CELLSIZE = 64
		self.ROOMSIZE = ((self.XCELLS) * self.CELLSIZE, (self.YCELLS) * self.CELLSIZE)

		self.gameSurf = pygame.Surface(self.ROOMSIZE)
		self.gameSurf = self.gameSurf.convert()

		self.gameRect = self.gameSurf.get_rect(center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2))

		self.dynamicObjects = pygame.sprite.Group()

		self.players  = pygame.sprite.Group()
		self.soldiers = pygame.sprite.Group()
		self.friendlyMobs = pygame.sprite.Group()

		self.heals = pygame.sprite.Group()


	def loadImage(self, filename):
		"""May be expanded later on for special effects"""
		img = pygame.image.load(filename)
		return img.convert_alpha()


	def saveGame(self):
		pass


	def pixToCells(self, pix):
		"""Convert pixel coords to cell coords"""
		return (int(math.floor(pix[0] / self.CELLSIZE)), int(math.floor(pix[1] / self.CELLSIZE)))


	def cellToPix(self, cell):
		"""Convert cell coords to pixel coords"""
		return (cell[0] * self.CELLSIZE, cell[1] * self.CELLSIZE)


if __name__ == '__main__':
	run()