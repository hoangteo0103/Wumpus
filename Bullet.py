import pygame

import pygame
import setting

class Bullet(pygame.sprite.Sprite):
	def __init__(self, nRow, nCol, curRow, curCol, dir):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/bullet.png')
		# self.image = pygame.transform.scale(self.image, (setting.BULLET_SIZE, setting.BULLET_SIZE))

		self.nRow = nRow
		self.nCol = nCol
		self.curRow = curRow
		self.curCol = curCol

		self.gridTopBound = int(setting.HEIGHT / 2 - self.nRow * setting.TILE_SIZE / 2)
		self.gridLeftBound = int(setting.WIDTH / 2 - self.nCol * setting.TILE_SIZE / 2)

		self.rect = self.image.get_rect()
		self.rect.centerx = self.gridLeftBound + self.curCol * setting.TILE_SIZE + setting.TILE_SIZE / 2
		self.rect.centery = self.gridTopBound + self.curRow * setting.TILE_SIZE + setting.TILE_SIZE / 2
		self.initCenterX = self.rect.centerx
		self.initCenterY = self.rect.centery

		self.speedx = 0
		self.speedy = 0
		if dir == 0:
			self.speedy = -setting.BULLET_SPEED
		elif dir == 1:
			self.speedx = setting.BULLET_SPEED
			self.image = pygame.transform.rotate(self.image, -90)
		elif dir == 2:
			self.speedy = setting.BULLET_SPEED
			self.image = pygame.transform.rotate(self.image, -180)
		else:
			self.speedx = -setting.BULLET_SPEED
			self.image = pygame.transform.rotate(self.image, -270)

	def update(self):
		self.rect.centerx += self.speedx
		self.rect.centery += self.speedy
		if abs(self.initCenterX - self.rect.centerx) > setting.TILE_SIZE * 1.25:
			self.kill()
		if abs(self.initCenterY - self.rect.centery) > setting.TILE_SIZE * 1.25:
			self.kill()
