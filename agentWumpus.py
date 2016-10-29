import updatewumpus
import FOPC

this_world = updatewumpus.intialize_world()
bindings = {}

maybee = {}

def is_safe_move(cell):
	try:
		guesses = maybee.get(cell)
		if guesses[0]:
			return False
		if guesses[1]:
			return False
		else:
			return True
	except:
		print 'We don\'t know anything about ',cell
		pass

this_cell = updatewumpus.take_action(this_world, "Up")
# for i in range(4):
# 	location = this_cell[5]
# 	statement = (this_cell[i], location)
# 	pattern = (this_cell[i], '?x')
# 	FOPC.match(statement, pattern, bindings)

nearby_cells = updatewumpus.look_ahead(this_world)
for cell in nearby_cells:
	maybe_wumpus = 1 if this_cell[0] == 'nasty' else 0
	maybe_pit = 1 if this_cell[1] == 'breeze' else 0
	maybee[cell] = [maybe_wumpus, maybe_pit]
safe_moves = []
for cell in nearby_cells:
	if is_safe_move(cell):
		safe_moves.append(cell)

for move in safe_moves:
	print move
	if int(move[-2]) > int(this_cell[5][-2]) & int(move[-1]) == int(this_cell[5][-2]):
		direction = 'Up'
	elif int(move[-2]) == int(this_cell[5][-2]) & int(move[-1]) < int(this_cell[5][-2]):
		direction = 'Left'
	elif int(move[-2]) == int(this_cell[5][-2]) & int(move[-1]) > int(this_cell[5][-2]):
		direction = 'Right'
	else:
		direction = 'Down'
	next_cell = updatewumpus.take_action(this_world, direction)
	next_cell = updatewumpus.take_action(this_world, 'Step')
