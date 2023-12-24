import pygame

import setting
import Agent
import Wumpus
import Pit
import Gold
import Bullet
import Exit

class Game:
	def __init__(self, board):
		pygame.init()
		self.screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
		self.clock = pygame.time.Clock()
		self.nRow = len(board)
		self.nCol = len(board[0])
		self.board = board
		self.gridTopBound = int(setting.HEIGHT / 2 - self.nRow * setting.TILE_SIZE / 2)
		self.gridLeftBound = int(setting.WIDTH / 2 - self.nCol * setting.TILE_SIZE / 2)
		self.gridBottomBound = self.gridTopBound + self.nRow * setting.TILE_SIZE
		self.gridRightBound = self.gridLeftBound + self.nCol * setting.TILE_SIZE
		
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


		self.bullet = pygame.sprite.Group()


	def run(self):
		self.running = True
		while self.running:
			self.dt = self.clock.tick(setting.FPS) / 1000
			self.events()
			self.update()
			self.draw()

		print('total points:', self.totalPoint)
		pygame.quit()

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

		if self.board[self.agent.curRow][self.agent.curCol] == 'G':
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

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.agentRotateLeft()
				elif event.key == pygame.K_RIGHT:
					self.agentRotateRight()
				elif event.key == pygame.K_UP:
					self.agentMoveForward()
				elif event.key == pygame.K_x:
					self.agentShot()

	def update(self):
		self.allSprites.update()
		self.bullet.update()

	def draw(self):
		self.screen.fill(setting.BACKGROUND_COLOR)
		self.allSprites.draw(self.screen)
		self.bullet.draw(self.screen)
		self.drawGrid()
		pygame.display.flip()

	def quit(self):
		self.running = False

	def drawGrid(self):
		for x in range(self.gridLeftBound, self.gridRightBound + 1, setting.TILE_SIZE):
			pygame.draw.line(self.screen, setting.BLACK, (x, self.gridTopBound), (x, self.gridBottomBound))

		for y in range(self.gridTopBound, self.gridBottomBound + 1, setting.TILE_SIZE):
			pygame.draw.line(self.screen, setting.BLACK, (self.gridLeftBound, y), (self.gridRightBound, y))

board = [['0', '0', '0', '0', '0', '0'],
		 ['0', 'S', '0', 'B', 'P', '0'],
		 ['0', 'W', 'SBG', 'P', 'B', '0'],
		 ['0', 'S', '0', 'B', '0', '0'],
		 ['0', 'A', 'B', 'P', 'B', '0'],
		 ['0', '0', '0', '0', '0', '0']]

game = Game(board)
game.run()