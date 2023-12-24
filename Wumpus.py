import pygame
import setting

class Wumpus(pygame.sprite.Sprite):
	def __init__(self, nRow, nCol, curRow, curCol):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/monster.png')
		# self.image = pygame.transform.scale(self.image, (setting.TILE_SIZE - setting.PADDING_AGENT, setting.TILE_SIZE - setting.PADDING_AGENT))

		self.nRow = nRow
		self.nCol = nCol
		self.curRow = curRow
		self.curCol = curCol

		self.gridTopBound = int(setting.HEIGHT / 2 - self.nRow * setting.TILE_SIZE / 2)
		self.gridLeftBound = int(setting.WIDTH / 2 - self.nCol * setting.TILE_SIZE / 2)

		self.rect = self.image.get_rect()
		self.rect.centerx = self.gridLeftBound + self.curCol * setting.TILE_SIZE + setting.TILE_SIZE / 2
		self.rect.centery = self.gridTopBound + self.curRow * setting.TILE_SIZE + setting.TILE_SIZE / 2

	def update(self):
		pass

	def setTransparency(self, val):
		self.image.set_alpha(val)
