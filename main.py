import pygame

from random import randrange, uniform
from time import sleep
from fontcontroller import FontController
from rendertext import RenderText

class Cell:
	def __init__(self,x,y,width,winx,winy):
		self.x = x
		self.y = y
		self.width = width
		self.color = "black"
		self.clicked = False
		self.value = None
		self.font_controller = FontController()
		self.valuetext = RenderText(self.font_controller, "black", "white")
		self.valuetext.update_x(self.x + self.width // 2)
		self.valuetext.update_y(self.y + self.width // 2)

	def __str__(self):
		return str(self.x) + "," + str(self.y)

	def render(self,screen):
		wid = self.width
		not_filled = 1 if not self.clicked else 0
		pygame.draw.rect(screen, self.color, (self.x,self.y,wid,wid), not_filled)

		if self.value is not None:
			self.valuetext.update_text(str(self.value))
			self.valuetext.draw(screen)

class Grid:
	def __init__(self):
		self.cells = []
		self.cell_size = 0
		self.clicked_cell = None

	def init(self,winx,winy):
		self.cells = []
		self.cell_size = 0
		x = 0
		y = 0
		self.cell_size = ((winx + winy) // 2) // 9
		for j in range(9):
			row = []

			for k in range(9):
				row.append(Cell(x,y,self.cell_size,winx,winy))
				x += self.cell_size

			self.cells.append(row)
			x = 0
			y += self.cell_size

	def part_valid(self):
		# Rows
		xset = set([])
		for row in self.cells:
			for cell in row:
				if not cell.value:
					continue
				if cell.value in xset:
					cell.value = None
					return False
				xset.add(cell.value)

		# Columns
		for row_id in range(9):
			xset = set([])
			for col_id in range(9):
				cell = self.cells[col_id][row_id]
				if not cell.value:
					continue
				if cell.value in xset:
					cell.value = None
					return False
				xset.add(cell.value)

		# Sections
		for ysection in range(3):
			for xsection in range(3):
				xs = xsection
				ys = ysection
				xset = set([])
				for col_id in range(3):
					for row_id in range(3):
						cell = self.cells[col_id + 3 * ys][row_id + 3 * xs]

						if not cell.value:
							continue

						if cell.value in xset:
							return False

						xset.add(cell.value)

		return True

	def validate_final(self):
		# total sum for any row or column
		xsum = 45

		# Add up the rows
		for row in self.cells:
			row_tot = 0
			for cell in row:
				if not cell.value:
					return False
				row_tot += cell.value

			if row_tot != xsum:
				return False

		# Add up the columns
		for row_id in range(9):
			ctot = 0
			for col_id in range(9):
				cell = self.cells[col_id][row_id]
				if not cell.value:
					return False
				ctot += cell.value
			if ctot != 45:
				return False

		# Add up the sections
		for ysection in range(3):
			for xsection in range(3):
				section_sum = 0
				xs = xsection
				ys = ysection
				for col_id in range(3):
					for row_id in range(3):
						cell = self.cells[col_id + 3 * ys][row_id + 3 * xs]

						if not cell.value:
							return False

						section_sum += cell.value

				if section_sum != 45:
					return False

		return True

	def render(self,surface,winx,winy):
		x = 0
		y = 0
		ctr = 0
		for row in self.cells:
			for cell in row:
				cell.render(surface)

			x += self.cell_size * 3
			if ctr == 3:
				ctr = 0
				y += self.cell_size * 3

			pygame.draw.line(surface, "black", (0,y), (winx,y), 4)
			pygame.draw.line(surface, "black", (x,0), (x,winy), 4)
			ctr += 1

def main(winx=900,winy=900):
	diff = 999
	while diff < 0 or diff > 3:
		print("Select a difficulty: 1 (easy), 2 (medium), 3 (hard)")
		diff = int(input(''))
		if diff < 0 or diff > 3:
			print(f"Not a valid difficulty: {diff}")

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))

	grid = Grid()
	font_controller = FontController()

	prepop_grid_portion = 1.0
	if diff == 1:
		prepop_grid_portion = 1.0
	elif diff == 2:
		prepop_grid_portion = 0.25
	elif diff == 3:
		prepop_grid_portion = 0.1

	grid.init(winx,winy)
	for row in grid.cells:
		for cell in row:
			# Assign grid values based on difficulty
			xv = uniform(0,1)
			if xv <= prepop_grid_portion:
				cell.value = randrange(1,10)

	res = grid.part_valid()
	# Whittle down the cells with values until there's a valid board
	while not res:
		res = grid.part_valid()

	# Start the game
	done = False
	while not done:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos
				xi = mx//grid.cell_size
				yi = my//grid.cell_size
				cell = grid.cells[yi][xi]
				if not cell.value and e.button == 1:
					cell.value = 1
				elif cell.value:
					if e.button == 1 and cell.value < 9:
						cell.value += 1
					elif e.button == 3:
						cell.value = max(0,cell.value - 1)
						if cell.value == 0:
							cell.value = None
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
