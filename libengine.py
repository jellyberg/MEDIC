# 
# a game by Adam Binks
import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)   # use a lower buffersize to reduce sound latency
pygame.init()
import input, game, math

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
		self.FPS = 120
		self.input = input.Input()


	def newGame(self):
		self.XCELLS, self.YCELLS = (24, 12)
		self.CELLSIZE = 64
		self.ROOMSIZE = (self.XCELLS * self.CELLSIZE, self.YCELLS * self.CELLSIZE)

		self.gameSurf = pygame.Surface(self.ROOMSIZE)
		self.gameSurf = self.gameSurf.convert()

		self.gameRect = self.gameSurf.get_rect(center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2))

		self.soldiers = pygame.sprite.Group()


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