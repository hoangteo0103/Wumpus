import pygame
import setting

class Agent(pygame.sprite.Sprite):
	def __init__(self, nRow, nCol, curRow, curCol):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/tank_64.png')
		self.image = pygame.transform.scale(self.image, (setting.TILE_SIZE - setting.PADDING_AGENT, setting.TILE_SIZE - setting.PADDING_AGENT))
		
		self.nRow = nRow
		self.nCol = nCol
		self.curRow = curRow
		self.curCol = curCol

		self.gridTopBound = int(setting.HEIGHT / 2 - self.nRow * setting.TILE_SIZE / 2)
		self.gridLeftBound = int(setting.WIDTH / 2 - self.nCol * setting.TILE_SIZE / 2)
		self.gridBottomBound = self.gridTopBound + self.nRow * setting.TILE_SIZE
		self.gridRightBound = self.gridLeftBound + self.nCol * setting.TILE_SIZE

		self.rect = self.image.get_rect()
		self.rect.centerx = self.getCenter(self.curRow, self.curCol)[0]
		self.rect.centery = self.getCenter(self.curRow, self.curCol)[1]
		self.faceDirection = 0
		self.rotateRight()

	def getCenter(self, row, col):
		x = self.gridLeftBound + col * setting.TILE_SIZE + setting.TILE_SIZE / 2
		y = self.gridTopBound + row * setting.TILE_SIZE + setting.TILE_SIZE / 2
		return (x, y)

	def update(self):
		self.rect.centerx = self.getCenter(self.curRow, self.curCol)[0]
		self.rect.centery = self.getCenter(self.curRow, self.curCol)[1]

	def moveForward(self):
		print("agent.moveForward")
		if self.faceDirection == 0:
			if self.curRow == 0:
				return False
			else:
				self.curRow -= 1
		elif self.faceDirection == 1:
			if self.curCol == self.nCol - 1:
				return False
			else:
				self.curCol += 1
		elif self.faceDirection == 2:
			if self.curRow == self.nRow - 1:
				return False
			else:
				self.curRow += 1
		else:
			if self.curCol == 0:
				return False
			else:
				self.curCol -= 1
		return True

	def rotateLeft(self):
		print("agent.rotateLeft")
		self.image = pygame.transform.rotate(self.image, 90)
		self.faceDirection = (self.faceDirection - 1 + 4) % 4

	def rotateRight(self):
		print("agent.rotateRight")
		self.image = pygame.transform.rotate(self.image, -90)
		self.faceDirection = (self.faceDirection + 1) % 4