class Solver:
	def __init__(self):
		pass

	def validate_final(self,board):
		# Add up the rows
		for row in board.cells:
			xset = set([])
			row_tot = 0
			for cell in row:
				if not cell.value:
					return False
				if cell.value in xset:
					return False
				xset.add(cell.value)

		# Add up the columns
		for row_id in range(9):
			xset = set([])
			for col_id in range(9):
				cell = board.cells[col_id][row_id]
				if not cell.value:
					return False
				if cell.value in xset:
					return False
				xset.add(cell.value)

		# Add up the sections
		for ysection in range(3):
			for xsection in range(3):
				xs = xsection
				ys = ysection
				xset = set([])
				for col_id in range(3):
					for row_id in range(3):
						cell = board.cells[col_id + 3 * ys][row_id + 3 * xs]

						if not cell.value:
							return False

						if cell.value in xset:
							return False

						xset.add(cell.value)

		return True
