import pygame

from random import randrange
from time import sleep

class Cell:
	def __init__(self,x,y,width,winx,winy):
		self.x = x
		self.y = y
		self.width = width
		self.color = "black"
		self.clicked = False

	def __str__(self):
		return str(self.x) + "," + str(self.y)

class Grid:
	def __init__(self):
		self.cells = []
		self.cell_size = 0

	def init(self,winx,winy):
		self.cells = []
		self.cell_size = 0
		x = 0
		y = 0
		self.cell_size = ((winx + winy) // 2) // 9
		print("cell_size",self.cell_size)
		for j in range(9):
			row = []

			for k in range(9):
				row.append(Cell(x,y,self.cell_size,winx,winy))
				x += self.cell_size

			self.cells.append(row)
			x = 0
			y += self.cell_size

	def render(self,surface,winx,winy):
		wid = self.cell_size
		x = 0
		y = 0
		ctr = 0
		for row in self.cells:
			for cell in row:
				#print("cell",cell.x,cell.y,wid)
				not_filled = 1 if not cell.clicked else 0
				pygame.draw.rect(surface, cell.color, (cell.x,cell.y,wid,wid), not_filled)

			x += self.cell_size * 3
			if ctr == 3:
				ctr = 0
				y += self.cell_size * 3

			pygame.draw.line(surface, "black", (0,y), (winx,y), 4)
			pygame.draw.line(surface, "black", (x,0), (x,winy), 4)
			ctr += 1

def main(winx=900,winy=900):
	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))

	grid = Grid()
	grid.init(winx,winy)

	done = False
	while not done:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos
				xi = mx//grid.cell_size
				yi = my//grid.cell_size
				print("cell indices",xi,yi)
				cell = grid.cells[yi][xi]
				cell.clicked = True
				cell.color = tuple([randrange(0,255) for i in range(3)])
			if e.type == pygame.QUIT:
				done = True
				break
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		if done:
			continue

		screen.fill("white")
		grid.render(screen,winx,winy)
		pygame.display.flip()
		sleep(0.25)

	pygame.display.quit()

if __name__ == "__main__":
	main()
