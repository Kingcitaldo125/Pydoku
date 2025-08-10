import os
import pygame

from json import loads
from random import choice, randrange, uniform
from time import sleep

from fontcontroller import FontController
from rendertext import RenderText

from grid import Cell,Grid
from solver import Solver

def flash_cell_color(screen,winx,winy,grid,cell,color,times=9):
	x = False
	screen.fill("white")
	grid.render(screen,winx,winy)
	for i in range(times):
		cell_bounds = (cell.x,cell.y,cell.width,cell.width)
		col = cell.color if x else color
		pygame.draw.rect(screen, col, cell_bounds, 1)

		if cell.value is not None:
			cell.valuetext.update_text(str(cell.value))
			cell.valuetext.draw(screen)

		pygame.display.flip()
		sleep(0.15)
		x = not x

def initialize_grid(winx, winy, pop_perc):
	grid = Grid()
	grid.init(winx,winy)
	total_cells = 81
	perc = total_cells - int(total_cells * pop_perc)

	# Select a random completed board to sample valid values from
	board_files = []
	datadir = './data'
	for path,dir,files in os.walk(datadir):
		board_files = files
		break

	file_choice = os.path.join(datadir,choice(board_files))
	board_data = None
	with open(file_choice) as f:
		board_data = loads(f.read())

	# Set the board cell values based on the values present in the chosen file
	bx = 0
	by = 0
	for row in grid.cells:
		bx = 0
		for cell in row:
			cell.value = board_data[by][bx]
			bx += 1
		by += 1

	# Whittle down the cells based on difficulty
	for i in range(perc):
		xcell = grid.cells[randrange(0,9)][randrange(0,9)]
		while xcell.value is None:
			xcell = grid.cells[randrange(0,9)][randrange(0,9)]
		xcell.value = None

	# Set the initially set cells
	grid.set_init()
	return grid

def main(winx=900,winy=900):
	diff = 999
	while diff < 0 or diff > 3:
		print("Select a difficulty: 1 (easy), 2 (medium), 3 (hard)")
		diff = int(input(''))
		if diff < 0 or diff > 3:
			print(f"Not a valid difficulty: {diff}")

	pygame.display.init()
	screen = pygame.display.set_mode((winx,winy))

	font_controller = FontController()
	solver = Solver()

	prepop_grid_portion = 0.8
	if diff == 1:
		prepop_grid_portion = 0.8
	elif diff == 2:
		prepop_grid_portion = 0.25
	elif diff == 3:
		prepop_grid_portion = 0.1

	grid = initialize_grid(winx, winy, prepop_grid_portion)

	# Start the game
	done = False
	valid = False
	while not done:
		events = pygame.event.get()
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx,my = e.pos
				xi = mx//grid.cell_size
				yi = my//grid.cell_size
				cell = grid.cells[yi][xi]

				# If this was one of the initially populated cells, don't process it
				if grid.is_init_cell(cell):
					flash_cell_color(screen,winx,winy,grid,cell,"red")
					continue

				if not cell.value and e.button == 1:
					cell.value = 1
				elif cell.value:
					if e.button == 1 and cell.value < 9:
						cell.value += 1
					elif e.button == 3:
						cell.value = max(0,cell.value - 1)
						if cell.value == 0:
							cell.value = None

				# Check to see if the game is complete
				valid = solver.validate_final(grid)
				if valid:
					done = True
					break
			elif e.type == pygame.QUIT:
				done = True
				break
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					done = True
					break

		if done:
			continue

		screen.fill("white")
		grid.render(screen,winx,winy)
		pygame.display.flip()
		sleep(0.25)

	if valid:
		print("You Win!")

		# Flashing green to signal a win condition
		screen.fill("white")
		grid.render(screen,winx,winy)
		x = False
		for i in range(9):
			for row in grid.cells:
				for cell in row:
					cell_bounds = (cell.x, cell.y, cell.width, cell.width)
					col = cell.color if x else "green"
					pygame.draw.rect(screen, col, cell_bounds, 1)

					if cell.value is not None:
						cell.valuetext.update_text(str(cell.value))
						cell.valuetext.draw(screen)

			pygame.display.flip()
			sleep(0.5)
			x = not x

		done = False
		while not done:
			events = pygame.event.get()
			for e in events:
				if e.type == pygame.QUIT:
					done = True
					break
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						done = True
						break

	pygame.display.quit()

if __name__ == "__main__":
	main()
