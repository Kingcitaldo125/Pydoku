import pygame

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
