import pygame

import setting
import Agent
import Wumpus
import Pit
import Gold
import Bullet
import Exit
import TextBox
import Sensor
from Action import *

class Game:
	def __init__(self, board, map):
		pygame.init()
		self.map = map
		self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
		pygame.display.set_caption('Wumpus project - SID: 21125020 - 21125161 - 21125027 - 21125171')
		self.clock = pygame.time.Clock()
		self.nRow = len(board)
		self.nCol = len(board[0])
		self.output = []
		self.board = board
		self.gridTopBound = int(setting.HEIGHT / 2 - self.nRow * setting.TILE_SIZE / 2)
		self.gridLeftBound = int(setting.WIDTH / 2 - self.nCol * setting.TILE_SIZE / 2)
		self.gridBottomBound = self.gridTopBound + self.nRow * setting.TILE_SIZE
		self.gridRightBound = self.gridLeftBound + self.nCol * setting.TILE_SIZE
		self.moveDir = ((0, -1), (0, 1), (-1, 0), (1, 0))
		
		self.initData()

	def getCenter(self, row, col):
		x = self.gridLeftBound + col * setting.TILE_SIZE + setting.TILE_SIZE / 2
		y = self.gridTopBound + row * setting.TILE_SIZE + setting.TILE_SIZE / 2
		return (x, y)

	def getFaceCell(self):
		row = self.agent.curRow
		col = self.agent.curCol
		if self.agent.faceDirection == 0 and row != 0:
			return (row - 1, col)
		if self.agent.faceDirection == 1 and col != self.nCol - 1:
			return (row, col + 1)
		if self.agent.faceDirection == 2 and row != self.nRow - 1:
			return (row + 1, col)
		if self.agent.faceDirection == 3 and col != 0:
			return (row, col - 1)
		return None

	def initData(self):
		self.totalPoint = 0
		self.font = pygame.font.Font('fonts/Roboto-Regular.ttf', 20)
		self.pointBox = TextBox.TextBox(f'score: {self.totalPoint}', self.font, self.gridLeftBound, self.gridTopBound - setting.TILE_SIZE)
		
		for i in range(self.nRow):
			for j in range(self.nCol):
				if len(self.board[i][j]) == 1:
					if self.board[i][j] == 'S' or self.board[i][j] == 'B':
						self.board[i][j] = '0'
				else:
					self.board[i][j] = self.board[i][j].replace('S', '')
					self.board[i][j] = self.board[i][j].replace('B', '')

		self.spriteBoard = [[0]*self.nCol for i in range(self.nRow)]
		self.allSprites = pygame.sprite.Group()
		for i in range(self.nRow):
			for j in range(self.nCol):
				if 'A' in self.board[i][j]:
					self.initAgentRow = i
					self.initAgentCol = j
					self.board[i][j] = '0'
				elif 'P' in self.board[i][j]:
					self.spriteBoard[i][j] = Pit.Pit(self.nRow, self.nCol, i, j)
				elif 'W' in self.board[i][j]:
					self.spriteBoard[i][j] = Wumpus.Wumpus(self.nRow, self.nCol, i, j)
				elif 'G' in self.board[i][j]:
					self.spriteBoard[i][j] = Gold.Gold(self.nRow, self.nCol, i, j)
				
				if self.spriteBoard[i][j] != 0:
					self.allSprites.add(self.spriteBoard[i][j])

		self.agent = Agent.Agent(
			self.nRow, self.nCol,
			self.initAgentRow, self.initAgentCol)
		self.allSprites.add(self.agent)
		self.allSprites.add(Exit.Exit(self.nRow, self.nCol, self.nRow, 0))

		self.perceptSprite = pygame.sprite.Group()
		self.wumpusPercept = Wumpus.Wumpus(self.nRow, self.nCol, -1, 1)
		self.perceptSprite.add(self.wumpusPercept)

		self.pitPercept = Pit.Pit(self.nRow, self.nCol, -1, 2)
		self.perceptSprite.add(self.pitPercept)

		self.perceptSprite.add(Sensor.Sensor(self.nRow, self.nCol, -1, 0))

		self.bullet = pygame.sprite.Group()


	def run(self, func, agent, kb):
		self.running = True
		while self.running:
			self.dt = self.clock.tick(setting.FPS) / 1000
			actions = func(agent, kb)
			self.events(actions)
			self.update()
			self.draw()

		print('total points:', self.totalPoint)
		self.display_final_score()
		pygame.time.delay(3000)
		pygame.quit()
		
	def display_final_score(self):
		self.screen.fill(setting.WHITE)
		font = pygame.font.SysFont('Arial', 36)
		text = font.render(f'Total Points: {self.totalPoint}', True, setting.BLACK)
		text_rect = text.get_rect(center=(setting.WIDTH // 2, setting.HEIGHT // 2))
		self.screen.blit(text, text_rect)
		pygame.display.flip()
        
	def agentRotateLeft(self):
		self.agent.rotateLeft()

	def agentRotateRight(self):
		self.agent.rotateRight()

	def agentMoveForward(self):
		if self.agent.curRow == self.nRow - 1 and self.agent.curCol == 0 and self.agent.faceDirection == 2:
			print("Climbed out")
			self.totalPoint += setting.MOVE_COST
			self.totalPoint += setting.CLIMB_COST
			self.quit()
			return

		if self.agent.moveForward():
			self.totalPoint += setting.MOVE_COST
		
	def agentMoveBackward(self):
		if self.agent.curRow == self.nRow - 1 and self.agent.curCol == 0 and self.agent.faceDirection == 0:
			print("Climbed out")
			self.totalPoint += setting.MOVE_COST
			self.totalPoint += setting.CLIMB_COST
			self.quit()
			return

		if self.agent.moveBackward():
			self.totalPoint += setting.MOVE_COST

	def agentShot(self):
		print("shot")
		bullet = Bullet.Bullet(self.nRow, self.nCol, self.agent.curRow, self.agent.curCol, self.agent.faceDirection)
		self.bullet.add(bullet)
		self.totalPoint += setting.SHOT_COST
		cell = self.getFaceCell()
		if cell != None and self.board[cell[0]][cell[1]] == 'W':
			print("kill wumpus")
			self.board[cell[0]][cell[1]] = '0'
			self.spriteBoard[cell[0]][cell[1]].kill()

	def checkNearWumpus(self):
		for dirRow, dirCol in self.moveDir:
			u = self.agent.curRow + dirRow
			v = self.agent.curCol + dirCol
			if u < 0 or u >= self.nRow:
				continue
			if v < 0 or v >= self.nCol:
				continue
			if self.board[u][v] == 'W':
				return True
		return False

	def checkNearPit(self):
		for dirRow, dirCol in self.moveDir:
			u = self.agent.curRow + dirRow
			v = self.agent.curCol + dirCol
			if u < 0 or u >= self.nRow:
				continue
			if v < 0 or v >= self.nCol:
				continue
			if self.board[u][v] == 'P':
				return True
		return False

	def events(self, actions):
		print("HEY" , actions, self.agent.faceDirection)
		for action in reversed(actions):
			old_action = action 
			if action == None:
				continue
			if action == SHOOT:
				self.agentShot()
				continue
			if action == LEFT:
				action = 3
			elif action == DOWN:
				action = 2
			elif action == RIGHT:
				action = 1
			elif action == UP:
				action = 0
			print("HEy1", action, old_action)
			if action > self.agent.faceDirection:
				for i in range(action - self.agent.faceDirection):
					self.agentRotateRight()
					self.output.append("RIGHT")
			else:
				for i in range(self.agent.faceDirection - action):
					self.agentRotateLeft()
					self.output.append("LEFT")

			self.agentMoveForward()
			self.output.append("FORWARD")
			self.update()
		
	def update(self):
		self.allSprites.update()
		self.bullet.update()

		self.pointBox = TextBox.TextBox(f'score: {self.totalPoint}', self.font, self.gridLeftBound, self.gridTopBound - setting.TILE_SIZE)

		if self.checkNearPit():
			self.pitPercept.setTransparency(setting.HIGH_OPACITY)
		else:
			self.pitPercept.setTransparency(setting.LOW_OPACITY)

		if self.checkNearWumpus():
			self.wumpusPercept.setTransparency(setting.HIGH_OPACITY)
		else:
			self.wumpusPercept.setTransparency(setting.LOW_OPACITY)


		if self.board[self.agent.curRow][self.agent.curCol] == 'G':
			print('pick up gold chess !!')
			self.totalPoint += setting.CHESS_COST
			self.board[self.agent.curRow][self.agent.curCol] = '0'
			self.spriteBoard[self.agent.curRow][self.agent.curCol].kill()

		if self.board[self.agent.curRow][self.agent.curCol] == 'W':
			print("killed by wumpus !!")
			self.totalPoint += setting.DIE_COST
			self.quit()

		if self.board[self.agent.curRow][self.agent.curCol] == 'P':
			print("killed by pit !!")
			self.totalPoint += setting.DIE_COST
			self.quit()

		if self.agent.curRow == self.nRow - 1 and self.agent.curCol == 0:
			self.quit()

	def draw(self):
		# print("current points:", self.totalPoint)
		self.screen.fill(setting.BACKGROUND_COLOR)
		self.allSprites.draw(self.screen)
		self.bullet.draw(self.screen)
		self.drawGrid()
		self.pointBox.draw(self.screen)
		self.perceptSprite.draw(self.screen)
		pygame.display.flip()

	def quit(self):
		file_path = self.map.replace(".txt", "_output.txt")
		# Open the file in write mode
		with open(file_path, "w") as file:
			# Use a for loop to write each string to the file
			file.write(str(self.totalPoint) + "\n")
			for string in self.output:
				file.write(string + "\n")
		self.running = False

	def drawGrid(self):
		for x in range(self.gridLeftBound, self.gridRightBound + 1, setting.TILE_SIZE):
			pygame.draw.line(self.screen, setting.BLACK, (x, self.gridTopBound), (x, self.gridBottomBound))

		for y in range(self.gridTopBound, self.gridBottomBound + 1, setting.TILE_SIZE):
			pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound, y), (self.gridRightBound, y))

		pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound, self.gridTopBound - setting.TILE_SIZE),
													 (self.gridLeftBound + setting.TILE_SIZE * 3, self.gridTopBound - setting.TILE_SIZE))
		pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound, self.gridTopBound),
													 (self.gridLeftBound + setting.TILE_SIZE * 3, self.gridTopBound))
		
		pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound, self.gridTopBound - setting.TILE_SIZE),
													 (self.gridLeftBound, self.gridTopBound))
		pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound + setting.TILE_SIZE, self.gridTopBound - setting.TILE_SIZE),
													 (self.gridLeftBound + setting.TILE_SIZE, self.gridTopBound))
		pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound + setting.TILE_SIZE * 3, self.gridTopBound - setting.TILE_SIZE),
													 (self.gridLeftBound + setting.TILE_SIZE * 3, self.gridTopBound))