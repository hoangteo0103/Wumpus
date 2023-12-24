import pygame
import setting

class TextBox(pygame.sprite.Sprite):
	def __init__(self, str, font, corX, corY, strColor = setting.BLACK, backColor = setting.BACKGROUND_COLOR):
		self.text = font.render(str, True, strColor, backColor)
		self.textRect = self.text.get_rect()
		self.textRect.bottom = corY
		self.textRect.right = corX

	def draw(self, screen):
		screen.blit(self.text, self.textRect)		
