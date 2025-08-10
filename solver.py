class Solver:
	def __init__(self):
		pass

	def validate_final(self,board):
		# total sum for any row or column
		xsum = 45

		# Add up the rows
		for row in board.cells:
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
				cell = board.cells[col_id][row_id]
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
						cell = board.cells[col_id + 3 * ys][row_id + 3 * xs]

						if not cell.value:
							return False

						section_sum += cell.value

				if section_sum != 45:
					return False

		return True
