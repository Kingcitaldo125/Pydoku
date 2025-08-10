import pygame

from random import randrange, uniform
from time import sleep

from fontcontroller import FontController
from rendertext import RenderText

from grid import Cell,Grid
from solver import Solver

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
	valid = False
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

				# Check to see if the game is complete
				valid = solver.validate_final(grid)
				if valid:
					done = True
					break
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

	if valid:
		x = False
		print("You Win!")
		for i in range(9):
			screen.fill("white")

			for row in grid.cells:
				for cell in row:
					cell_bounds = (cell.x,cell.y,cell.width,cell.width)
					col = cell.color if x else "green"
					pygame.draw.rect(screen, col, cell_bounds, 1)

					if self.value is not None:
						self.valuetext.update_text(str(self.value))
						self.valuetext.draw(screen)

			pygame.display.flip()
			sleep(0.5)
			x = not x

	done = False
	while not done:
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
