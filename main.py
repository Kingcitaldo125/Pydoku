import pygame

from random import randrange, uniform
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
	solver = Solver()

	prepop_grid_portion = 0.8
	if diff == 1:
		prepop_grid_portion = 0.8
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

	# Set the initially set cells
	grid.set_init()

	'''
	popcells = [
	[2,8,1,4,5,9,6,3,7],
	[5,3,4,7,6,1,2,8,9],
	[9,7,6,8,3,2,1,4,5],
	[1,2,3,5,4,7,9,6,8],
	[7,6,9,3,1,8,4,5,2],
	[8,4,5,9,2,6,3,7,1],
	[6,5,7,2,9,4,8,1,3],
	[4,9,8,1,7,3,5,2,6],
	[None, None, None, None, None, None, None, None, None]
	]

	ictr = 0
	jctr = 0
	for row in grid.cells:
		jctr = 0
		for cell in row:
			cell.value = popcells[ictr][jctr]
			jctr += 1
		ictr += 1
	'''

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
