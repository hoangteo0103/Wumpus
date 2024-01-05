import pygame
import setting
class MenuPygame: 
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
		self.font = pygame.font.SysFont('Georgia', 30)
        
class button(MenuPygame):
	#colours for button and text
	button_col = (255, 0, 0)
	hover_col = (75, 225, 255)
	click_col = (50, 150, 255)
	text_col = setting.BLACK
	width = 180
	height = 70

	def __init__(self, x, y, text):
		super().__init__()
		self.x = x
		self.y = y
		self.text = text
		self.clicked = False

	def draw_button(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
		button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
		
		#check mouseover and clicked conditions
		if button_rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = True
				pygame.draw.rect(self.screen, self.click_col, button_rect)
			elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
				self.clicked = False
				action = True
			else:
				pygame.draw.rect(self.screen, self.hover_col, button_rect)
		else:
			pygame.draw.rect(self.screen, self.button_col, button_rect)
		
		#add shading to button
		pygame.draw.line(self.screen, setting.WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
		pygame.draw.line(self.screen, setting.WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
		pygame.draw.line(self.screen, setting.WHITE, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
		pygame.draw.line(self.screen, setting.WHITE, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

		#add text to button
		text_img = self.font.render(self.text, True, self.text_col)
		text_len = text_img.get_width()
		self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 20))
		return action

class Menu():
	def __init__(self):
		print("hihi")
		pygame.init()
		self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
		self.list_button = []
		for i in range(5):
			self.list_button.append(button(setting.WIDTH/2 - 90, 100 + i*100, f'Map {i+1}'))
		pygame.display.set_caption('Wumpus project - SID: 21125020 - 21125161 - 21125027 - 21125171')
		self.background_image = pygame.image.load('images/background.png')
		self.background_image = pygame.transform.scale(self.background_image, (setting.WIDTH, setting.HEIGHT))
		self.font = pygame.font.SysFont('Georgia', 30)		
		self.map = 1
			
	def run(self):
		run = True
		while run: 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
			self.screen.blit(self.background_image, (0, 0))
			for i in range(5):
				if self.list_button[i].draw_button():
					print('MAP ' + str(i+1))
					self.map = f'map{i+1}' + '.txt'
					run = False
			pygame.display.update()
			

                
                

            
                

            

            
            






	


